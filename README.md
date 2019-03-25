# LINE_BOT


## 步驟 


### Step 1 前置作業:

下載測試資料

[MongoData](https://drive.google.com/open?id=1MUAS-78v7ucQAZK9gA_jOr92VsnFXLRI)

```angular2
upzip mongoData
chmod 777 -R mongoData
```

更改 docker-compose 內容

```
command: start-notebook.sh --NotebookApp.token="TOKEN"
```

填入想要的 Token 之後登入 jupyter notebook 要用

```
command: ngrok http --authtoken TOKEN jupyter:5000
```

輸入 Ngrok Token ; 若無 就刪除 `--auth.... TOKEN`

``` 
KAFKA_ADVERTISED_LISTENERS: INSIDE://kafka:9093,OUTSIDE://IP_SERVER:9092
```

填入 目前 Server IP

```
- MONGODB_PASSWORD=PASSWORD
```

填入 MongoDB 密碼 

```
mkdir portainer_data
chmod 777 -R portainer_data
chmod 777 -R mongoData
sh start.sh
```


#### 修改 Mysql 密碼 及 host

打開 `Code/MyUtil/mysql_account.py`

##### MongoDB

```
MongoBase password = "PASSWORD"
```

輸入剛才docker-compose 內的MongoDB密碼

##### MySQL

```
MyAccount host = db host
account = db account
passwd = db password
```

### Step 2:

打開 `Code/line_secret_key`

填入對應的資訊

打開 `Code/Step 1-regist_Menu.ipynb`

Run 到 上傳圖片完成為止

確認 `Code/line_secret_key` 是否完成更改

rich_menu_id 的部分

打開 `Code/Step 2.py`

更改所有資料庫連線 `MySQLdb.connect()` 如果需要


```angular2
sh start-server.sh
```

### 關閉Server 及 Container

```angular2
sh stop.sh
```
