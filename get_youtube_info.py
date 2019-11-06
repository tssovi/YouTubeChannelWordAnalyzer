import requests
import json


class GetYoutubeInfo():

	def __init__(self):
		# Credentials and Variables
		self.api_key = "REPLACE_ME_WITH_YOUR_PERSONAL_API_KEY"
		self.youtube_base_api_url = "https://www.googleapis.com/youtube/v3/"
		self.youtube_channel_api_url = self.youtube_base_api_url + "channels?key={0}&".format(self.api_key)
		self.youtube_search_api_url = self.youtube_base_api_url + "search?key={0}&".format(self.api_key)

		self.request_to_get_channel_info_for_name = self.youtube_channel_api_url + "forUsername={0}&part=snippet"
		self.request_to_get_channel_info_for_id = self.youtube_channel_api_url + "id={0}&part=snippet"
		self.request_to_get_video_ids = self.youtube_search_api_url + "channelId={0}&part=id&order=date&type=video&pageToken={1}&maxResults=50"

		self.get_channel_info_logs = []
		self.get_all_video_ids_logs = []

	def get_channel_info(self, channel_filter):
		channel_id = ""
		channel_name = ""
		error_domain = ""
		error_reason = ""
		error_message = ""
		
		url_for_name = self.request_to_get_channel_info_for_name.format(channel_filter)
		url_for_id = self.request_to_get_channel_info_for_id.format(channel_filter)

		response = requests.get(url_for_name).json()

		try:
			check_errors = response["error"]["errors"]

			if check_errors:
				error_domain = check_errors[0]["domain"]
				error_reason = check_errors[0]["reason"]
				error_message = check_errors[0]["message"]
				flag = "error"
				return error_domain, error_reason, error_message, flag

		except:
			message = "Searching channel id for channel: {0}.".format(channel_filter)
			self.get_channel_info_logs.append(message)

			try:
				if(response["pageInfo"]["totalResults"] < 1):
					response = requests.get(url_for_id).json()
				
				if(response["pageInfo"]["totalResults"] > 0):
					channel_info = response["items"][0]
					channel_id = channel_info["id"]
					channel_name = channel_info["snippet"]["title"]
					message = "\nFounded YouTube Channel Info\n-----------------------------\nChannel ID : {0}\nChannel Name: {1}\n".format(channel_id, channel_name)
					self.get_channel_info_logs.append(message)
				else:
					message = "Response received but it contains no item."
					self.get_channel_info_logs.append(message)
					message = "The channel id could not be retrieved.Please make sure that the channel name is correct."
					self.get_channel_info_logs.append(message)

				if(response["pageInfo"]["totalResults"] > 1):
					message = "Multiple channel id were received in the response."
					self.get_channel_info_logs.append(message)
			except Exception:
				message = "An exception occurred while trying to retrieve the channel id."
				self.get_channel_info_logs.append(message)
			flag = "success"
			return channel_id, channel_name, self.get_channel_info_logs, flag


	def get_all_video_ids(self, channel_id):
		video_ids = []
		next_page_token = ""
		error_domain = ""
		error_reason = ""
		error_message = ""
		flag = ""
		
		url = self.request_to_get_video_ids.format(channel_id, next_page_token)

		response = requests.get(url).json()

		try:
			check_errors = response["error"]["errors"]

			if check_errors:
				error_domain = check_errors[0]["domain"]
				error_reason = check_errors[0]["reason"]
				error_message = check_errors[0]["message"]
				flag = "error"
				return error_domain, error_reason, error_message, flag

		except:
			message = "Searching video id(s) for channel id: {0}.".format(channel_id)
			self.get_all_video_ids_logs.append(message)
			while True:
				response = requests.get(url).json()
				items = response["items"]

				for item in items:
					if item["id"]["kind"] == "youtube#video":
						video_ids.append(item["id"]["videoId"])

				try:
					next_page_token = response["nextPageToken"]
					url = request_to_get_video_ids.format(channel_id, next_page_token)
				except:
					if len(video_ids) > 0:
						message = "All possible video id(s) are acquired."
						self.get_all_video_ids_logs.append(message)
					else:
						message = "Either no video for this {} channel is uploaded or provided an invalid channel id.".format(channel_id)
						self.get_all_video_ids_logs.append(message)
					break
			# Get and return only unique video id(s)
			video_ids = set(video_ids)
			flag = "success"
			return video_ids, self.get_all_video_ids_logs, "", flag

