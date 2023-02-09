def create_command(data, path):
    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        data["source_url"],
    ]

    if "rtsp" in data:
        cmd.append('-rtsp_transport')
        cmd.append(data['rtsp']['rtsp_transport'])

    if "strftime" in data and data['strftime']:
        cmd.append('-strftime')
        cmd.append('1')

    if "mapping" in data:
        mapping = data['mapping']
        if "map" in mapping:
            cmd.append('-map')
            cmd.append(data['mapping']['map'])
        if "c_a" in mapping:
            cmd.append('-c:a')
            cmd.append(data['mapping']['c_a'])
        if "c_v" in mapping:
            cmd.append('-c:v')
            cmd.append(data['mapping']['c_v'])

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
        cmd.append(path + "/%Y-%m-%dT%H:%M:%S%z.ts")

        cmd.append(path + "/index.m3u8")

    return cmd

