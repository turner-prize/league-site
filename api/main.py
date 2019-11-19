
from waitress import serve
import config


connex_app = config.connex_app
connex_app.add_api("swagger.yml")

if __name__ == '__main__':
	connex_app.run(host='0.0.0.0', port=3000,debug=True)
    #serve(connex_app,host='0.0.0.0',port=3000)