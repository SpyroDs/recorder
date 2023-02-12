# Run:
/usr/local/bin/python3.9 /path/to/main.py -u test -p pass -c /var/records

# Boot on start and reload on fails
sudo tee /etc/systemd/system/recorder.service >/dev/null << EOF
[Unit]
Wants=network.target
Description=Video Recorder
[Service]
ExecStart=/usr/bin/python3 /usr/local/src/recorder/main.py -s 127.0.0.1 -r 5000 -u myuser -p mypass -c /var/records
Restart=on-failure
RestartSec=1s
[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable recorder
sudo systemctl start recorder

# POST
```json
{
    "source_url": "rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mp4",
    "hls": {
        "hls_time": 10,
        "hls_list_size": 0,
        "hls_flags": [
            "independent_segments"
        ],
        "hls_segment_type": "fmp4"
    },
    "strftime": true,
    "mapping": {
        "map": "0:v",
        "c_a": "aac",
        "c_v": "copy"
    },
    "rtsp": {
        "rtsp_transport": "tcp"
    }
}
```