import uvicorn

if __name__ == '__main__':
    #uvicorn.run("main:app",
    #            host="0.0.0.0",
    #            port=8986,
    #            reload=True,
    #            ssl_keyfile="./de.key",
    #            ssl_certfile="./de.cert"
    #           )
    uvicorn.run("main:app",
                host="0.0.0.0",
                port=8986,
                reload=True,
                )