def create_command(data, path):
    cmd = [
        "ffmpeg",
        "-y",
    ]

    if "loglevel" in data:
        cmd.append('-loglevel')
        cmd.append(data['loglevel'])

    if "rtsp" in data:
        cmd.append('-rtsp_transport')
        cmd.append(data['rtsp']['rtsp_transport'])
        if "rtbufsize" in data['rtsp']:
            cmd.append('-rtbufsize')
            cmd.append(data['rtsp']['rtbufsize'])

    if "timeout" in data:
        cmd.append('-timeout')
        cmd.append(str(data['timeout']))

    if "err_detect" in data:
        cmd.append('-err_detect')
        cmd.append(data['err_detect'])

    cmd.append('-i')
    cmd.append(data["source_url"])

    if "fps_mode" in data:
        cmd.append('-fps_mode')
        cmd.append(data['fps_mode'])

    if "strftime" in data and data['strftime']:
        cmd.append('-strftime')
        cmd.append('1')

    if "analyzeduration" in data:
        cmd.append('-analyzeduration')
        cmd.append(str(data['analyzeduration']))

    if "mapping" in data:
        mapping = data['mapping']
        if "map" in mapping:
            for m in data['mapping']['map']:
                cmd.append('-map')
                cmd.append(m)
        if "c_a" in mapping:
            cmd.append('-c:a')
            cmd.append(data['mapping']['c_a'])
        if "c_v" in mapping:
            cmd.append('-c:v')
            cmd.append(data['mapping']['c_v'])

    if "vprofile" in data:
        cmd.append('-vprofile')
        cmd.append(data['vprofile'])

    if "segment" in data:
        segment = data['segment']

        cmd.append('-f')
        cmd.append('segment')

        # format
        cmd.append('-segment_format')
        if "segment_format" in segment:
            cmd.append(segment['segment_format'])
        else:
            cmd.append('mp4')

        # type
        cmd.append('-segment_list_type')
        if "segment_list_type" in segment:
            cmd.append(segment['segment_list_type'])
        else:
            cmd.append('m3u8')

        # size
        cmd.append('-segment_list_size')
        if "segment_list_size" in segment:
            cmd.append(str(segment['segment_list_size']))
        else:
            cmd.append('10')

        # segment duration
        if "segment_time" in segment:
            cmd.append('-segment_time')
            cmd.append(str(segment['segment_time']))

        # list file name
        cmd.append('-segment_list')
        if "segment_list" in segment:
            cmd.append(path + "/" + segment['segment_list'])
        else:
            cmd.append('index.m3u8')

        # output file
        cmd.append(path + "/" + segment['segment_file'])

    if "hls" in data:
        segment_ext = 'ts'
        hls = data['hls']

        cmd.append('-f')
        cmd.append('hls')

        if "hls_time" in hls:
            cmd.append('-hls_time')
            cmd.append(str(hls['hls_time']))
        if "hls_list_size" in hls:
            cmd.append('-hls_list_size')
            cmd.append(str(hls['hls_list_size']))
        if "hls_flags" in hls:
            flags = []
            for flag in hls['hls_flags']:
                flags.append(flag)
            cmd.append('-hls_flags')
            cmd.append("+".join(flags))
        if "hls_segment_type" in hls:
            cmd.append('-hls_segment_type')
            cmd.append(hls['hls_segment_type'])
            if hls['hls_segment_type'] == 'fmp4':
                segment_ext = 'm4s'

        cmd.append('-hls_segment_filename')
        cmd.append(path + "/%Y-%m-%dT%H_%M_%S." + segment_ext)

        cmd.append(path + "/index.m3u8")


    return cmd

