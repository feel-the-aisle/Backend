from flask import Flask, Blueprint, request, jsonify
from service import find_service as fc

app = Flask(__name__)

# Blueprint 객체 생성
jindongMap_bp = Blueprint('path', __name__)


# 라우트 등록하기
@jindongMap_bp.route('/find_shortest_path', methods=['POST'])
def find_shortest_path():
          data = request.get_json()  # POST로 전송된 JSON 데이터 받기
          storeName = data['name']
          startP = data['startPoint']
          endP = data['endPoint']

          result = fc.find_shortest_path(storeName, startP, endP)
        #   # path 값 = 연산 결과 예시
        #   result = [(1, 8), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7),
        #             (6, 6), (6, 5), (6, 4), (6, 3), (6, 2), (5, 2), (4, 2),
        #             (3, 2), (3, 1), (2, 1)]

          return jsonify({'result': result})


# 실제 연산 부분
def jindongMap_result(storeName, startP, endP):
          # 지도의 가로, 세로 규격 가져오기
          size = fc.get_maze_size(storeName)
          galo = size[0]
          selo = size[1]

          # 지도 만들기
          maze = fc.create_maze(storeName, galo, selo)

          # 출발, 도착 지점 가져오기
          points = fc.get_start_end(startP, endP, selo, galo, maze)
          # [0]: 출발 가로 / [1]: 출발 세로 / [2]: 도착 가로 / [3]: 도착 세로
          start = (points[1], points[0])
          end = (points[3], points[2])

          # 경로 찾기
          path = fc.find_shortest_path(maze, start, end)
          return path