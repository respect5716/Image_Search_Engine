# Image Search Engine
Image search engine using pretrained MobileNetv2 and Elasticsearch



## Execute

```shell
git clone https://github.com/respect5716/Image_Search_Engine.git
cd Image_Search_Engine
docker-compose up
```



The first time you run it, you need to put data in the Elasticsearch. The images in the **images/** directory are uploaded if you run the code below in the web container CLI.

```
python prepare.py
```



If you have memory error when using Elasticsearch, try this.

Windows

```powershell
wsl -d docker-desktop
sysctl -w vm.max_map_count=262144
```

Linux

```shell
sudo sysctl -w vm.max_map_count=262144
```



## Result

![](result.png)