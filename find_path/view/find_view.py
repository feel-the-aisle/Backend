from flask import Blueprint, request, jsonify
from find_path.service.find_service import Findservice, find_shortest_path

# Blueprint 객체 생성
findpath_bp = Blueprint('findpath_bp', __name__)

# 라우트 등록하기
@findpath_bp.route('/find_paths', methods=['POST'])
def find_paths():
  data = request.get_json()  # POST로 전송된 JSON 데이터 받기
  storeName = data['name']
  startP = data['startPoint']
  endP = data['endPoint']

  size = Findservice.get_maze_size(storeName) 
  maze = Findservice.create_maze(storeName, size[0], size[1])
  points = Findservice.get_start_end(startP, endP, size[1], size[0], maze)
  start = (points[1], points[0]) 
  end = (points[3], points[2])

  result = find_shortest_path(maze, start, end)
  strPath = Findservice.list_to_str_path(result)
  direction = Findservice.get_end_direction(result)
  endPosition = Findservice.check_position(direction, size[1], size[0], end, maze, endP)
  return jsonify({'result': result, 'strPath': strPath, 'endPosition': endPosition, 'storeSelo': size[1], 'storeGalo': size[0]})


@findpath_bp.route('/connect_dbtest_path', methods=['GET'])
def dummy():
  map = Findservice.test_maze()
  size = Findservice.test_size()  
  selo = size[0]
  galo = size[1]
  points = Findservice.get_start_end("음료", "과자", selo, galo, map)
  start = (points[1], points[0])
  end = (points[3], points[2])

  result = find_shortest_path(map, start, end)
  strPath = Findservice.list_to_str_path(result)
  direction = Findservice.get_end_direction(result)
  endPosition = Findservice.check_position(direction, selo, galo, end, map, "과자")
  return jsonify({'result': result, 'strPath': strPath, 'endPosition': endPosition, 'sizeSelo': size[1], 'sizeGalo': size[0]})