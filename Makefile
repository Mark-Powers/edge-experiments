build:
	docker build --platform linux/arm64 . -t mppowers/power_measurement:latest

push:
	docker push mppowers/power_measurement:latest
