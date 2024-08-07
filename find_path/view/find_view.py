from flask import Blueprint, request, jsonify
from find_path.service.find_service import Detectservice, find_shortest_path

# Blueprint 객체 생성
findpath_bp = Blueprint('findpath_bp', __name__)

# 라우트 등록하기
@findpath_bp.route('/find_paths', methods=['POST'])
def find_paths():
  data = request.get_json()  # POST로 전송된 JSON 데이터 받기
  storeName = data['name']
  startP = data['startPoint']
  endP = data['endPoint']

  size = Detectservice.get_maze_size(storeName) 
  maze = Detectservice.create_maze(storeName, size[0], size[1])
  points = Detectservice.get_start_end(startP, endP, size[1], size[0], maze)
  start = (points[1], points[0]) 
  end = (points[3], points[2])
  oriend = (points[5], points[4])   
  result = find_shortest_path(maze, start, end)
  strPath = Detectservice.list_to_str_path(result)

  coordinate = Detectservice.set_three_position(maze, start, end)
  direction = Detectservice.get_end_direction(coordinate)
  endPosition = Detectservice.compare_coordinates(direction, oriend, end)
  return jsonify({'result': result, 'strPath': strPath, 'endPosition': endPosition})


# # 실제 연산 부분
# def setup_map_and_positions(storeName, startP, endP):
#   size = Detectservice.get_maze_size(storeName) # 지도의 가로, 세로 규격 가져오기

#   maze = Detectservice.create_maze(storeName, size[0], size[1]) # 지도 만들기

#   points = Detectservice.get_start_end(startP, endP, size[1], size[0], maze) # 출발, 도착 지점 가져오기
#   start = (points[1], points[0]) # [0]: 출발 가로, [1]: 출발 세로
#   end = (points[3], points[2])   # [2]: 도착 가로, [3]: 도착 세로

#   path = find_shortest_path(maze, start, end) # 경로 찾기 
#   return path



# test용
@findpath_bp.route('/connect_dbtest_path', methods=['GET'])
def dummy():
  map = Detectservice.test()  
  points = Detectservice.get_start_end("음료", "카운터", 16, 16, map)
  start = (points[1], points[0]) 
  end = (points[3], points[2])
  oriend = (points[5], points[4])   

  result = find_shortest_path(map, start, end)
  # path 값 = 연산 결과 예시
  #  result = [(1, 8), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7),
  #             (6, 6), (6, 5), (6, 4), (6, 3), (6, 2), (5, 2), (4, 2),
  #             (3, 2), (3, 1), (2, 1)]

  strPath = Detectservice.list_to_str_path(result)

  coordinate = Detectservice.set_three_position(maze, start, end)
  direction = Detectservice.get_end_direction(coordinate)
  endPosition = Detectservice.compare_coordinates(direction, oriend, end)
  return jsonify({'result': result, 'strPath': strPath, 'endPosition': endPosition})
