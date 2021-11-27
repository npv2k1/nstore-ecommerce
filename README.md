# **ECOMMERCE**

Các phiên bản phần mềm:

```bash
λ python --version
Python 3.8.8
λ node --version
v16.13.0
λ docker-compose -v
docker-compose version 1.29.2, build 5becea4c
```

Mọi người có thể sử dụng `docker` để thiệt lập môi trường phát triển nhanh hơn không cần cài các phần mềm khác

Các công nghệ sử dụng

**Client:** React,, TailwindCSS, NextJS

**Server:** Django, Mysql


Cấu trúc thư mục của dự án

## Cách cài đặt và bắt đầu

### **server**

Đây là backend viết bằng django nó nằm ở thư mục [server](./server) của dự án. Để di chuyển vào thư mục ta sử dụng lệnh sau:

```bash
cd server
```

Dự án sử dụng pipenv để quản lý các package nếu chưa có `pipenv` thì cài `pipenv` bằng lệnh sau:

```bash
  pip install pipenv
```

Cái đặt package

```bash
  pipenv install
```

* Nếu bị lỗi liên quan đến phiên bản python có thể vào file [Pipfile](./server/Pipfile) và thay đổi `python_version` nhưng yêu cầu python 3
* Một số package có thể không cài được trên windows.

Chạy

```bash
  pipenv shell
  python manage.py runserver 5000
```

* Trang web sẽ chạy ở cổng 5000 nếu cổng 5000 đã có ứng dụng khác sử dụng thì có thể thay đổi thành cổng khác

* Nếu sử dụng `gunicon`. gunicon chỉ hỗ trợ các hệ thông unix nên trên windows nó sẽ bị lỗi. Để khắc phục có thể chạy trên hệ thông `WSL` hoặc sử dụng docker.

  ```bash
  gunicorn --bind 0.0.0.0:5000 --workers 4 --worker-class nstore.asgi.gunicorn_worker.UvicornWorker nstore.asgi:application
  ```

Khởi tạo dữ liệu ban đầu:

```bash
cd server
python manage.py migrate
python manage.py loaddata upload.json 
python manage.py loaddata groups.json 
python manage.py loaddata categories.json 
python manage.py loaddata order_status.json 
```

* Khi load dữ liệu cần đảm bảo thứ tự. groups, uploads, categories.json, products, order_status vì một số cái yêu cầu quan hệ nên có cần có dữ liệu trước.

Thu thập tệp tĩnh:

```bash
python manage.py collectstatic
```



### **client**

Đây là client viết bằng nextjs nó nằm ở thư mục [client](./client) của dự án. Để di chuyển vào thư mục ta sử dụng lệnh sau:

```bash
cd client
```

Cài đặt các package

```bash
  yarn install
```

chạy

```bash
  yarn dev
```

* Trang web sẽ chạy ở cổng 3000

* Có 2 biến môi trường cần lưu ý

  ```json
  # Api này sẽ được gọi khi web chạy ở client
  NEXT_PUBLIC_REST_API_ENDPOINT="http://localhost:5000/" 
  # Api này sẽ gọi trong quá trình xây dựng.
  NEXT_PUBLIC_SSR_REST_API_ENDPOINT="http://localhost:5000/"
  ```

  

### **database**

Mặc định sẽ dùng cơ sở dữ liệu `sqlite`. Nếu muốn chuyển qua `mysql` cần vào file [settings.py](./server/storefront/settings.py) để cài đặt. Hoặc thiết lập biến môi trường của server:

```json
DB_PROVIDER="mysql"
```

Dữ liệu được lưu trong thư mục `data`. Sử dụng docker để chạy csdl lên.

```bash
  docker-compose up -d
```
