from flask import Flask, request, jsonify
from db_model.mysql import db, ConvenienceStoreInfo, ConvenienceStoreMap



# 플루터-플라스크
app = Flask(__name__)


class Node:

  def __init__(self, parent=None, position=None):
    self.parent = parent
    self.position = position

    self.g = 0
    self.h = 0
    self.f = 0

  def __eq__(self, other):
    return self.position == other.position

def cost_check(node, goal, D=1):  # 상하좌우에 대한 가중치
  # node: 현재 노드, position- 현재 노드의 위치를 지칭하는 것
  # goal: 목표 노드(도착 지점)
  # D: 상하좌우 이동에 대한 비용계산. = 1
  left_right = abs(node.position[0] - goal.position[0])
  top_bottom = abs(node.position[1] - goal.position[1])
  return D * (left_right + top_bottom)

# 경로 찾기
def find_shortest_path(maze, start, end):
  # 시작/ 도착 지점 초기화
  startNode = Node(None, start)
  endNode = Node(None, end)
  # 저장 경로 초기화(reserve = 계산 중 / final = 결정된 것)
  reserveList = []
  finalList = []
  # reserveList에 시작 노드 추가
  reserveList.append(startNode)
  # 도착 지점을 찾을 때까지 실행 ( endNode 찾기까지 샐행 )
  while reserveList:
    # 현재 노드 지정
    currentNode = reserveList[0]
    currentIdx = 0

    # 이미 같은 노드가 reserveList에 있고, f 값이 더 크면
    # currentNode를 reserveList안에 있는 값으로 교체
    for index, item in enumerate(reserveList):
      if item.f < currentNode.f:
        currentNode = item
        currentIdx = index
    # reserveList에서 제거 후 finalList에 추가
    reserveList.pop(currentIdx)
    finalList.append(currentNode)
    # 현재 노드가 목적지면 current.position 추가하고
    # current의 부모로 이동
    if currentNode == endNode:
      path = []
      current = currentNode
      while current is not None:
        path.append(current.position)
        current = current.parent
      return path[::-1]  # reverse
    children = []
    # 인접한 xy좌표 상하좌우
    for newPosition in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
      # 노드 위치 추가
      nodePosition = (
          currentNode.position[0] + newPosition[0],  # X
          currentNode.position[1] + newPosition[1])  # Y
      # maze index 범위 안에 있어야함
      within_range_criteria = [
          nodePosition[0] > (len(maze) - 1),
          nodePosition[0] < 0,
          nodePosition[1] > (len(maze[len(maze) - 1]) - 1),
          nodePosition[1] < 0,
      ]
      # 하나라도 true면 범위 밖
      if any(within_range_criteria):
        continue
      # 장애물 판단후 이동
      # <진열대> 라면 : 1 / 음료 : 2 / 과자 : 3 / 기타 : 4
      #          카운터 : 5 / 입구 : 6
      if maze[nodePosition[0]][nodePosition[1]] in [1, 2, 3, 4, 5]:
        continue
      new_node = Node(currentNode, nodePosition)
      children.append(new_node)
    # 자식 loop
    for child in children:
      # 자식이 finalList에 있으면 진행
      if child in finalList:
        continue
      # f, g, h값 업데이트
      child.g = currentNode.g + 1
      child.h = cost_check(child, endNode)  #코스트 계산 값
      child.f = child.g + child.h
      # 자식이 reserveList에 존재 && g 값이 더 크면 진행
      if len([
          openNode for openNode in reserveList
          if child == openNode and child.g > openNode.g
      ]) > 0:
        continue
      reserveList.append(child)


class Detectservice:
  # 지도의 가로, 세로 규격 전역 변수에 저장 (row: 가로, col: 세로)
  @staticmethod
  def get_maze_size(storeName):
    storeN = ConvenienceStoreInfo.query.filter_by(storename = storeName).first()
    row = storeN.storerow
    col = storeN.storecol
    result = [row, col]
    return result


  # 지도 만들기
  @staticmethod
  def create_maze(storeName, galo, selo):
    # 지도 초기 규격 만들기
    storeId = ConvenienceStoreInfo.query.filter_by(storename=storeName).first()
    ids = storeId.id

    storeMaze = [[0] * galo for i in range(selo)]

    storeMap2 = ConvenienceStoreMap.query.filter_by(storeinfoid = ids).all()
    
    for storeMap in storeMap2:
      row = storeMap.storex
      col = storeMap.storey
      sangte = storeMap.storestate

      storeMaze[col][row] = sangte

    return storeMaze


  # 출발, 도착 지점 가져오기 (편의점 이름, 지점 선택 번호(출,도 int))
  # 배열 RETURN -> 0: 출발 가로 / 1: 출발 세로 / 2: 도착 가로 / 3: 도착 세로
  @staticmethod
  def get_start_end(startP, endP, storeSelo, storeGalo, storeMaze):
    strStart = startP
    strEnd = endP
    selo = storeSelo
    galo = storeGalo
    maze = storeMaze
    num1 = 0
    num2 = 0

    # 지점 리스트 가져오기
    if strStart == "라면" or strStart == "라면 진열대" or strStart == "라면진열대":
      num1 = 1
    elif strStart == "음료" or strStart == "음료 진열대" or strStart == "음료진열대":
      num1 = 2
    elif strStart == "과자" or strStart == "과자 진열대" or strStart == "과자진열대":
      num1 = 3
    elif strStart == "기타" or strStart == "기타 진열대" or strStart == "기타진열대":
      num1 = 4
    elif strStart == "카운터":
      num1 = 5
    elif strStart == "입구":
      num1 = 6

    if strEnd == "라면" or strEnd == "라면 진열대" or strEnd == "라면진열대":
      num2 = 1
    elif strEnd == "음료" or strEnd == "음료 진열대" or strEnd == "음료진열대":
      num2 = 2
    elif strEnd == "과자" or strEnd == "과자 진열대" or strEnd == "과자진열대":
      num2 = 3
    elif strEnd == "기타" or strEnd == "기타 진열대" or strEnd == "기타진열대":
      num2 = 4
    elif strEnd == "카운터":
      num2 = 5
    elif strEnd == "입구":
      num2 = 6

    # 각 리스트의 값을 활용하여 지점의 x, y좌표를 계산한다.
    calcullateGalo1 = 0
    calcullateSelo1 = 0
    count1 = 0
    calcullateGalo2 = 0
    calcullateSelo2 = 0
    count2 = 0

    # 가로, 세로 끼리 각각 총합, 총 개수
    for i in range(selo):
      for j in range(galo):
        if maze[i][j] == num1:
          calcullateGalo1 += j
          calcullateSelo1 += i
          count1 += 1
        if maze[i][j] == num2:
          calcullateGalo2 += j
          calcullateSelo2 += i
          count2 += 1

    # 중간 지점 계산하기.
    pointGalo1 = int(calcullateGalo1 / count1)  # 출발 지점의 가로 중간
    pointSelo1 = int(calcullateSelo1 / count1)  # 출발 지점의 세로 중간
    pointGalo2 = int(calcullateGalo2 / count2)  # 도착 지점의 가로 중간
    pointSelo2 = int(calcullateSelo2 / count2)  # 도착 지점의 세로 중간

    oriGalo = pointGalo2
    oriSelo = pointSelo2

    # 각 지점의 값이 움직임이 가능한 부분인지 확인하기
    # <<< 가중치 순서 [ 1 우 ][ 2 좌 ][ 3 하 ][ 4 상 ] >>>
    # 출발 가로 좌표에 대한 검사.
    if pointGalo1 == galo - 1:
      pointGalo1 -= 1
    elif pointGalo1 == 0:
      pointGalo1 += 1

    # 출발 세로 좌표에 대한 검사
    if pointSelo1 == selo - 1:
      pointSelo1 -= 1
    elif pointSelo1 == 0:
      pointSelo1 += 1

    # 도착 가로 좌표에 대한 검사
    if pointGalo2 == galo - 1:
      pointGalo2 -= 1
    elif pointGalo2 == 0:
      pointGalo2 += 1

    # 도착 세로 좌표에 대한 검사
    if pointSelo2 == selo - 1:
      pointSelo2 -= 1
    elif pointSelo2 == 0:
      pointSelo2 += 1

    # 출발지점 좌표 확인하기
    if maze[pointSelo1][pointGalo1] != 0:
      if maze[pointSelo1][pointGalo1 + 1] == 0:  # 우.
        pointGalo1 += 1
      elif maze[pointSelo1][pointGalo1 - 1] == 0:  # 좌
        pointGalo1 -= 1
      elif maze[pointSelo1 + 1][pointGalo1] == 0:  # 하
        pointSelo1 += 1
      elif maze[pointSelo1 - 1][pointGalo1] == 0:  # 상
        pointSelo1 -= 1

    # 도착지점 좌표 확인하기
    if maze[pointSelo2][pointGalo2] != 0:
      if maze[pointSelo2][pointGalo2 + 1] == 0:  # 우
        pointGalo2 += 1
      elif maze[pointSelo2][pointGalo2 - 1] == 0:  # 좌
        pointGalo2 -= 1
      elif maze[pointSelo2 + 1][pointGalo1] == 0:  # 하
        pointSelo2 += 1
      elif maze[pointSelo2 - 1][pointGalo1] == 0:  # 상
        pointSelo2 -= 1

    arr = []
    arr.append(pointGalo1)
    arr.append(pointSelo1)
    arr.append(pointGalo2)
    arr.append(pointSelo2)
    arr.append(oriGalo)
    arr.append(oriSelo)
    return arr
  

  #-------------- 도착 지점으로 부터 진열대의 위치 판단 --------------
  def set_three_position(maze, start, end):
    coordinates= find_shortest_path(maze, start, end)
    threeElements= coordinates[-3:]
    threeElements= coordinates[len(coordinates) - 3:]
    return threeElements
  

  def get_end_direction(arr):
    # [0]: 3 / [1]: 2 / [2]: 1
    x= [cor[0] for cor in arr]
    y= [cor[1] for cor in arr]
    dum= 0

    if x[0] == x[1]:      # 3, 2번 x좌표 비교
      if y[0] < y[1]:     # 3, 2번 y좌표 비교 ( - )
        dum = 2           # y증가 방향이 정면임을 의미
      else:               # 3, 2번 y좌표 비교 ( - )
        dum = 1           # y감소 방향이 정면임을 의미

      if x[1] == x[2]:    # 2, 1번 x좌표 비교
        dum = dum
      elif x[1] < x[2]:   # 2, 1번 x좌표 비교 ( + )
          dum = 4
      else:               # 2, 1번 x좌표 비교 ( - )
          dum = 3

    elif x[0] < x[1]:     # 3, 2번 x좌표 비교 ( + )
      dum = 4
      if x[1] == x[2]:    # 2, 1번 x좌표 비교
        if y[1] < y[2]:   # 2, 1번 y좌표 비교 ( + )
          dum = 2
        else:
          dum = 1

    else:                 # 3, 2번 x좌표 비교 ( - )
      dum = 3
      if x[1] == x[2]:
        if y[1] < y[2]:
          dum = 2
        else:
         dum = 1

    return dum
  

  def compare_coordinates(dum, e1, e2):
    s =""
    if dum == 1:
      s= "x 감소 방향 (뒤에꺼)"
    elif dum == 2:
      s= "x 증가 방향 (뒤에꺼)"
    elif dum == 3:
      s= "y 감소 방향 (위에꺼)"
    else:
      s= "y 증가 방향 (위에꺼)"
  
    n1 = e1[0]
    n2 = e1[1]
    m1 = e2[0]
    m2 = e2[1]
    strPosition =""
    if dum == 1:    # x 감소
      if n1 == m1:            # y 값 같다.
        if n2 < m2:           # x 비교
          strPosition ="정면에 위치합니다."
      else:                   # y값 다르다.
        if n1 < m1:
          strPosition ="오른쪽에 위치합니다."
        else:
          strPosition ="왼쪽에 위치합니다."

              
    elif dum == 2:  # x 증
      if n1 == m1:
          strPosition ="정면에 위치합니다."
      else:
        if n1 < m1:
          strPosition ="왼쪽에 위치합니다."
        else:
          strPosition ="오른쪽에 위치합니다."


    elif dum == 3:  # y 감
      if n2 == m2:
        strPosition ="정면에 위치합니다."
      else:
        if n2 < m2:
          strPosition ="오른쪽에 위치합니다."
        else:
          strPosition ="왼쪽에 위치합니다."

    elif dum == 4:  # y 증

      if n2 == m2:
        strPosition ="정면에 위치합니다."
      else:
        if n2 < m2:
          strPosition ="왼쪽에 위치합니다."
        else:
          strPosition ="오른쪽에 위치합니다."
    return strPosition


  def list_to_str_path(path):
    # 경로 저장 리스트
    listPath = []
    # 상대성 저장 , 이동 횟수 확인(보류)
    relativity = 0
    count_move = 0

    for i in range(1, len(path)):
      prev= path[i-1]   # 과거
      curr= path[i]     # 현재

      # 상대성 판단하기
      # 1: y down   2: y up   3: x down   4: x up
      if i == 1:
        if curr[0] == prev[0]:  # < y좌표 -> 같다 >
          if curr[1] < prev[1]:  # x좌표 :: 현재 위치 < 이전 위치 == x 감소
            relativity = 3
          elif curr[1] > prev[1]:  # x좌표 :: 현재 위치 > 이전 위치 == x 증가
            relativity = 4
        elif curr[1] == prev[1]:  # < x좌표 -> 같다 >
          if curr[0] < prev[0]:  # y좌표 :: 현재 위치 < 이전 위치 == y 감소
            relativity = 1
          elif curr[0] > prev[0]:  # y좌표 :: 현재 위치 > 이전 위치 == y 증가
            relativity = 2

      # 상대성에 따른 이동 listPath에 저장
      if relativity == 1:  # y 감소 (위)
        if curr[1] == prev[1]:  # x좌표가 같다면 y방향에 변동 없음
          if not listPath or listPath[-1] != "직진":
            listPath.append("직진")
        if curr[1] < prev[1]:  # x값 현재 < 과거 // y감소 방향 (위)에서 x값 감소 (왼쪽)
          listPath.append("좌회전")
        elif curr[1] > prev[1]:
          listPath.append("우회전")

      elif relativity == 2:  # y 증가 (아래)
        if curr[1] == prev[1]:  # x좌표가 같다면 y방향에 변동 없음
          if not listPath or listPath[-1] != "직진":
            listPath.append("직진")
        if curr[1] < prev[1]:  # x값 현재 < 과거 // y증가 방향 (아래)에서 x값 증가 (오른쪽)
          listPath.append("우회전")
        elif curr[1] > prev[1]:
          listPath.append("좌회전")

      elif relativity == 3:  # x 감소 (좌)
        if curr[0] == prev[0]:  # y좌표가 같다면 y방향에 변동 없음
          if not listPath or listPath[-1] != "직진":
            listPath.append("직진")
        if curr[0] < prev[0]:  # y값 현재 < 과거 // x감소 방향 , y값 감소 (오른쪽)
          listPath.append("우회전")
        elif curr[0] > prev[0]:
          listPath.append("좌회전")

      elif relativity == 4:  # x 증가 (우)
        if curr[0] == prev[0]:  # y좌표가 같다면 y방향에 변동 없음
          if not listPath or listPath[-1] != "직진":
            listPath.append("직진")
        if curr[0] < prev[0]:  # y값 현재 < 과거 // x증가 방향 , y값 감소 (왼쪽)
          listPath.append("좌회전")
        elif curr[0] > prev[0]:
          listPath.append("우회전")

      # 상대성 판단하기 relativity
      # 1: y 감소 | 2: y 증가 | 3: x 감소 | 4: x 증가
      if curr[0] == prev[0]:  # < y좌표 -> 같다 >
        if curr[1] < prev[1]:  # x좌표 :: 현재 위치 < 이전 위치 == x 감소
          relativity = 3
        elif curr[1] > prev[1]:  # x좌표 :: 현재 위치 > 이전 위치 == x 증가
          relativity = 4
      elif curr[1] == prev[1]:  # < x좌표 -> 같다 >
        if curr[0] < prev[0]:  # y좌표 :: 현재 위치 < 이전 위치 == y 감소
          relativity = 1
        elif curr[0] > prev[0]:  # y좌표 :: 현재 위치 > 이전 위치 == y 증가
          relativity = 2

    return listPath

  #-------------- connect db test --------------
  def test():
    storeId = ConvenienceStoreInfo.query.filter_by(storename="미래혁신관").first()
    ids = storeId.id

    storeMaze = [[0] * storeId.storerow for i in range(storeId.storecol)]
    storeMaze = [ [0] * 16 for i in range(16)]
    storeMap2 = ConvenienceStoreMap.query.filter_by(storeinfoid = ids).all()
    
    for storeMap in storeMap2:
      row = storeMap.storex
      col = storeMap.storey
      sangte = storeMap.storestate

      storeMaze[col][row] = sangte
    return storeMaze