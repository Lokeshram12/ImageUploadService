import os
import tornado.web
import tornado.ioloop

# Define the handler for uploading images
class UploadImgHandler(tornado.web.RequestHandler):
    def get(self):
        # Render the HTML form for uploading files
        self.write("""
            <!DOCTYPE html>
            <html>
            <body>
                <h2>Upload Image</h2>
                <form action="/" method="post" enctype="multipart/form-data">
                    <input type="file" name="fileImage" accept="image/*">
                    <button type="submit">Upload</button>
                </form>
            </body>
            </html>
        """)

    def post(self):
        # Get the uploaded files
        if "fileImage" not in self.request.files:
            self.write("No file uploaded")
            return
        
        files = self.request.files["fileImage"]
        for file in files:
            # Save the uploaded file
            file_path = os.path.join("upload", file.filename)
            with open(file_path, "wb") as fh:
                fh.write(file.body)
            self.write(f"File uploaded successfully! Access it at: <a href='/img/{file.filename}'>/img/{file.filename}</a><br>")

# Main entry point for the Tornado application
if __name__ == "__main__":
    # Ensure the upload directory exists
    os.makedirs("upload", exist_ok=True)
    
    # Define the application with routes
    app = tornado.web.Application([
        ("/", UploadImgHandler),
        ("/img/(.*)", tornado.web.StaticFileHandler, {"path": "upload"}),  # Serve uploaded images
    ])
    
    # Start the server
    app.listen(8080)
    print("Server started at http://localhost:8080")
    tornado.ioloop.IOLoop.current().start()
