from flask import Blueprint, request, jsonify
from search_recipes.service.search_service import SearchService
from urllib.parse import quote

search_bp = Blueprint('search_bp', __name__)

# 엔드포인트 요청

@search_bp.route('/recipes', methods=['POST'])
def get_recipe():
    data = request.get_json()
    ramen = data['request_ramen']
    # 검색어 설정 및 URL 인코딩
    ramen_name = quote(ramen + " 조리법")
    
    # 블로그 출처, 블로그 글
    blog_contents, blog_links = SearchService.get_recipe(ramen_name)
    gpt_ramen_recipe = SearchService.gpt_ramen(ramen_name, blog_contents)
    
    return jsonify(
      {"recipe": gpt_ramen_recipe,
       "links": blog_links
       }
      ), 201