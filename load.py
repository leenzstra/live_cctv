import yadisk
y = yadisk.YaDisk(token="AQAAAAAcHEhbAAfYk8DaJ8UVEUggrKLR1wBBQ0M")
print(y.check_token()) 
#y.mkdir("/test")


def load_file(file_path, file_name, upload_to="test"):
    y.upload(file_path, f'/{upload_to}/{file_name}') 

