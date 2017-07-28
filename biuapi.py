from flask_restful import Resource, reqparse, abort, Api
from flask import Flask,jsonify, request
from biu import Aduit,HandleTarget,BiuPlugin
import sys
app = Flask(__name__)
api = Api(app, catch_all_404s=True)


class Scan(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('f', help='目标文件: 每行一个ip或域名')
        parser.add_argument('t', help='目标: example.com或233.233.233.233')
        parser.add_argument('r', help='ip范围: 233.233.233.0/24')
        parser.add_argument('p', help='插件名称', default='plugins')
        parser.add_argument('ps', help='插件搜索')
        parser.add_argument('d', help='Debug', default=0)
        parser.add_argument('T', help='超时时间', default=3)
        args = parser.parse_args()
        searchstr = args.get("p")
        plugins = BiuPlugin(searchstr=searchstr).plugins
        targets_file = args.get("f")
        iprange = args.get("r")
        target = args.get("t")
        debug = int(args.get("d"))
        timeout = int(args.get("T"))
        targets = HandleTarget(plugins=plugins, target=target,
                               iprange=iprange, targets_file=targets_file)
        results = []
        for task in targets.tasks:
            task = Aduit(task.get('url'),
                                 task.get('plugin'), timeout, debug)
            results.append(task.result)
        response = {
            'total': len(results),
            'results': results
        }
        return jsonify(response)


api.add_resource(Scan, '/api/task/new')

if __name__ == '__main__':
    app.run(debug=False, threaded=True, port=int(sys.argv[1]), host='0.0.0.0', use_reloader=True)

