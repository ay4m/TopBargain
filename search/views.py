from rest_framework.response import Response
from rest_framework.decorators import api_view

from posts.models import PostModel
from search.serializers import PostSerializer

@api_view(['GET'])
def search_view(request, query):
	query = query.replace('-', ' ')
	search_list = {'recommendedPrice': 0, 'list': []}
	final_list = {}

	if query is not None:
		query_set = PostModel.objects.filter(productName__icontains=query)

		total_price = 0

		for q in query_set:
			serialized = PostSerializer(q)
			serialized = dict(serialized.data)
			total_price += serialized['price']

			if str(q.image) is not '':
				path = str(q.image).split('TopBargain/')[1]
				serialized['image'] = path
				print(path)

			search_list['list'].append(serialized)

		if(len(query_set) > 0):
			search_list['recommendedPrice'] = int(total_price / len(query_set))

		final_list['searchResults'] = search_list

	return Response(final_list)