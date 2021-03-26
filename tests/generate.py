import qrcode

data = "Hello world"
qr = qrcode.make(data=data)
qr.save("tests/hello.png")