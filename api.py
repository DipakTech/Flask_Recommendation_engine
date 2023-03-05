from flask import Flask, jsonify,request
from flask_cors import CORS
import pickle
import numpy as np
# import bson from

app = Flask(__name__)
CORS(app)

userRating=pickle.load(open('userRating.pkl','rb'))
df=pickle.load(open('df.pkl','rb'))
similarity_score=pickle.load(open('similarity_score.pkl','rb'))

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  return response

@app.route('/api/get-products', methods=['GET','POST'])
def get_products():
  # data = request.get_json()
  text_data = request.args.get('text')
  print(text_data)
  index=np.where(userRating.index==text_data)[0][0]
  similar_items=sorted(list(enumerate(similarity_score[index])),key=lambda x:x[1],reverse=True)[1:6]
  data = []
  for i in similar_items:
      item = []
      temp_df = df[df['product'] == userRating.index[i[0]]]
      item.extend(list(temp_df.drop_duplicates('product')['product'].values))
      item.extend(list(temp_df.drop_duplicates('product')['rating'].values))
      item.extend(list(temp_df.drop_duplicates('product')['product_id'].values))
      item.extend(list(temp_df.drop_duplicates('product')['image'].values))
      item.extend(list(temp_df.drop_duplicates('product')['price'].values))
      data.append(item)
  print(data);
  objects = []
  for item in data:
    obj = {
      'name': item[0],
     'rating': int(item[1]),
      'id': str(item[2]),
      'image': str(item[3]),
      'price': item[4],
      }
    objects.append(obj)
  print(objects)
  # return {'data': objects}
  return jsonify(objects)

if __name__ == '__main__':
    app.run(debug=True, port=8001)