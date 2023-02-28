schema = {
    "$schema": "http://json-schema.org/draft-4/schema#",
    "type": "object",
    "additionalProperties": False,
    "required": [
        "source_url",
    ],
    "properties": {
        "additionalProperties": False,
        "restream": {
            "additionalProperties": False,
            "required": [
                "path",
                "port"
            ],
            "properties": {
                "path": {
                    "type": "string",
                    "pattern": "^([a-zA-Z0-9\\-\\_]){5,40}$",
                },
                "port": {
                    "type": "number"
                }
            }
        },
        "source_url": {
            "format": "uri",
            "type": "string",
            "pattern": "^(rtsp|rtsps|http|https)?://",
        },
        "strftime": {"type": "boolean"},
        "fps_mode": {
            "type": "string",
            "enum": [
                "passthrough",
                "cfr",
                "vfr",
                "drop",
                "auto"
            ]
        },
        "timeout": {
            "type": "number",
        },
        "analyzeduration": {
            "type": "number"
        },
        "vprofile": {
            "type": "string",
            "enum": [
                "high",
                "unknown",
                "main",
                "baseline"
            ]
        },
        "mapping": {
            "additionalProperties": False,
            "properties": {
                "c_a": {
                    "type": "string",
                    "enum": [
                        "aac",
                        "copy"
                    ]
                },
                "c_v": {
                    "type": "string",
                    "enum": [
                        "copy",
                        "h264",
                        "h265",
                        "libx264",
                        "libx265",
                    ]
                },
                "map": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "enum": [
                            "0:v",
                            "0:a",
                            "a:0",
                            "v:0",
                            "0:a:0",
                            "0:v:0",
                        ]
                    }
                }

            }
        },
        "loglevel": {
            "type": "string",
            "enum": [
                "quiet",
                "panic",
                "fatal",
                "warning",
                "info",
                "verbose",
                "debug",
                "trace",
            ]
        },
        "segment": {
            "additionalProperties": False,
            "properties": {
                "segment_format": {
                    "type": "string",
                    "enum": [
                        "mp4",
                        "mkv",
                        "mp3",
                        "aac"
                    ]
                },
                "segment_list": {
                    "type": "string",
                    "pattern": "^([a-zA-Z0-9\\_])+\\.([0-9a-z]){2,4}$",
                },
                "segment_file": {
                    "type": "string",
                    "pattern": "^([a-zA-Z0-9\\%\\-\\_])+\\.([0-9a-z]){2,4}$",
                },
                "segment_list_type": {
                    "type": "string",
                    "enum": [
                        "flat",
                        "csv, ext",
                        "ffconcat",
                        "m3u8",
                    ]
                },
                "segment_time": {
                    "type": "number"
                },
                "segment_list_size": {
                    "type": "number"
                },
                "segment_wrap": {
                    "type": "number"
                },
            },
        },
        "hls": {
            "additionalProperties": False,
            "properties": {
                "hls_time": {
                    "type": "number",
                },
                "hls_list_size": {
                    "type": "number"
                },
                "hls_flags": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "enum": [
                            "single_file",
                            "delete_segments",
                            "append_list",
                            "round_durations",
                            "discont_start",
                            "omit_endlist",
                            "periodic_rekey",
                            "independent_segments",
                            "iframes_only",
                            "split_by_time",
                            "program_date_time",
                            "second_level_segment_index",
                            "second_level_segment_size",
                            "second_level_segment_duration",
                        ]
                    },
                },
                "hls_segment_type": {
                    "type": "string",
                    "enum": ["fmp4", "mpegts"]
                }
            },

        },
        "rtsp": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "rtsp_transport": {
                    "type": "string",
                    "enum": ["tcp", "udp"]
                },
                "rtbufsize": {
                    "type": "string",
                    "enum": [
                        "100M",
                        "200M",
                        "500M",
                        "1G",
                        "2G",
                    ]
                },
            },
        },
    },
}
