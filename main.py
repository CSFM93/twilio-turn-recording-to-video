import subprocess


def run_command(command):
    p = subprocess.run(command,                  
    shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    print('Done!!!')
    print('stdout:\n{}'.format(p.stdout.decode()))
    print('stderr: {} \n \n'.format(p.stderr))
    return p.stdout.decode().strip()


def get_rec_duration(rec_name):
    rec_path = "./recordings/{}".format(rec_name)

    command = "ffprobe -i {rec_path} -show_entries format=duration -v quiet \
    -of csv=\"p=0\"".format(rec_path=rec_path)

    rec_duration = run_command(command)
    print("rec duration", rec_duration)

    return rec_duration


def turn_audio_to_video(rec_name,rec_duration):
    rec_path = "./recordings/{}".format(rec_name)
    bg_image_path = "./images/bg.png"
    video_name = "video_with_sound_waves.mp4"

    command = "ffmpeg -y -i {rec_path} -loop 1 -i {bg_image_path} -t {rec_duration} \
    -filter_complex \"[0:a]showwaves=s=1280x150:mode=cline:colors=00e5ff[fg];  \
    drawbox=x=0:y=285:w=1280:h=150:color=black@0.8:t=fill[bg]; \
    [bg][fg]overlay=format=auto:x=(W-w)/2:y=(H-h)/2 \" \
    -map 0:a -c:v libx264 -preset fast -crf 18 -c:a aac -shortest ./videos/{video_name}".format(
    rec_path=rec_path, bg_image_path=bg_image_path,
    rec_duration=rec_duration,video_name=video_name)
    
    print(video_name)
    run_command(command)
    return video_name


def add_spinning_record(video_name,rec_duration):
    video_path = "./videos/{}".format(video_name)
    spinning_record_video_path = "./videos/spinningRecord.mp4"
    new_video_name = "video_with_spinning_record.mp4"

    command = "ffmpeg -y -i {video_path} -stream_loop -1 -i {spinning_record_video_path} \
    -t {rec_duration} -filter_complex \"[1:v]scale=w=200:h=200[fg]; \
    [0:v] scale=w=1280:h=720[bg], [bg][fg]overlay=x=25:y=(H-225)\" \
    -c:v libx264 -preset fast -crf 18 -c:a copy ./videos/{new_video_name}".format(                              
    video_path=video_path, spinning_record_video_path=spinning_record_video_path,
    rec_duration=rec_duration, new_video_name=new_video_name)

    print(new_video_name)
    run_command(command)
    return new_video_name


def add_text_to_video(video_name):
    video_path = "./videos/{}".format(video_name)
    new_video_name = "video_with_text.mp4"
    font_path = "./fonts/LeagueGothic-CondensedRegular.otf"

    command = "ffmpeg -y -i {video_path} -vf \"drawtext=fontfile={font_path}:  \
    text='Turning your Twilio voice recordings into videos':fontcolor=black: \
    fontsize=90:box=1:boxcolor=white@0.5:boxborderw=5:x=((W/2)-(tw/2)):y=100\" \
    -c:a copy ./videos/{new_video_name}".format(video_path=video_path,font_path=font_path,
    new_video_name=new_video_name)
    
    print(new_video_name)
    run_command(command)
    return new_video_name


def main():
    rec_name = "rec_1.mp3"
    rec_duration = get_rec_duration(rec_name)
    video_with_sound_waves = turn_audio_to_video(rec_name,rec_duration)
    video_with_spinning_record = add_spinning_record(video_with_sound_waves,rec_duration)
    video_with_text = add_text_to_video(video_with_spinning_record)


main()




