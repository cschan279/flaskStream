# Problem to Solve
Here 3 main problem to be solve in the folder.

## Unexpected exit when unplug the camera
serve:
```
Camera.py --> main.py
```
view:
```
templates/index.html
main.py --> @app.route('/')
```
hoping to be able to resume the camera without restart or interrupt the program
the camera.read() just hold for a long period without return a (False,None)

## Include cv image in json (python)✓
```
imgJson-test.py
```

## Extract and display image from json (js)✓
```
templates/test-json-img.html
imgJson-test.py --> @app.route('/')
```


