# Run:
```shell
/usr/local/bin/python3.9 /path/to/main.py -u test -p pass -c /var/records
```

# Boot on start and reload on fails
```
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
```

```
sudo systemctl daemon-reload &
sudo systemctl enable recorder
sudo systemctl start recorder

sudo systemctl daemon-reload & sudo systemctl restart recorder
```
