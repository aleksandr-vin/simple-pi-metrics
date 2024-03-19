# Simple Raspberry Pi metrics service

```shell
python3 -m venv .venv
sudo ln -s $HOME/raspberrypi_metrics.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable raspberrypi_metrics.service
sudo systemctl start raspberrypi_metrics.service
```
