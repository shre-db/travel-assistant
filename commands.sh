# Docker commands
docker run \
    -d \
    --name traveller-gpu-cont \
    --shm-size 64G \
    --gpus all \
    -net=host \
    -p 5000:8000
    -v $(pwd):/workspace \
    -u $(id -u):$(id -g) \
    -e HOME=/workspace \
    -it traveller-gpu-img \
    bash