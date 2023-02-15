def create_command(data, path):
    cmd = [
        "ffmpeg",
        "-y",
    ]

    if "rtsp" in data:
        cmd.append('-rtsp_transport')
        cmd.append(data['rtsp']['rtsp_transport'])
        if "rtbufsize" in data['rtsp']:
            cmd.append('-rtbufsize')
            cmd.append(data['rtsp']['rtbufsize'])

    if "timeout" in data:
        cmd.append('-timeout')
        cmd.append(str(data['timeout']))

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

    if "hls" in data:
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

        cmd.append('-hls_segment_filename')
        cmd.append(path + "/%Y-%m-%dT%H:%M:%S%z.m4s")

        cmd.append(path + "/index.m3u8")

    return cmd

