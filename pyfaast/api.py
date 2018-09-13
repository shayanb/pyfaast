import requests
import threading
import pyfaast.constants as constants
import pyfaast.errors as errors


class Faast(object):

    def __init__(self, XAuthToken=None, proxies=None , TESTNET = False):
        self._session = requests.Session()
        self._session.headers.update(constants.HEADERS)
        self._token = XAuthToken
        self._proxies = proxies
        self._testnet = TESTNET
        if XAuthToken is not None:
            self._session.headers.update({"X-Auth-Token": str(XAuthToken)})

    def _full_url(self, url):
        _url = url.lower()

        if _url.startswith("http://") or _url.startswith("https://"):
            return url
        else:
            if self._testnet:
                return constants.TEST_BASE + url
            return constants.API_BASE + url

    def auth(self):
        data = {}
        result = self._session.post(
            self._full_url('/auth'), json=data, proxies=self._proxies)
        # if 'token' not in result:
        #     raise errors.RequestError("Couldn't authenticate")
        # self._token = result['token']
        # self._session.headers.update({"X-Auth-Token": str(result['token'])})
        return result

    def _request(self, method, url, data={}, debug = False):
        # if not hasattr(self, '_token'):
        #     raise errors.InitializationError
        result = self._session.request(method, self._full_url(url), json=data, proxies=self._proxies)
        if debug:
            print(self._full_url(url))
            print(result.status_code)
            print (result.content)
        while result.status_code == 429:
            blocker = threading.Event()
            blocker.wait(0.01)
            result = self._session.request(method, self._full_url(
                url), data=data, proxies=self._proxies)
        if result.status_code < 200 or result.status_code >= 300:
            raise errors.RequestError(result.status_code)
        if result.status_code == 201 or result.status_code == 204:
            return {}
        return result.json()



    def get_pair_price(self, pair = "BTC_ETH", url = "/api/v2/public/price/"):
        if not url.endswith("/"):
            url = url + "/" + pair
        else:
            url = url + pair
        print (url)
        return self._request("GET", url, debug = True)


    def _pair_split(self, pair):
        deposit_currency, withdrawal_currency = pair.split("_")
        print (deposit_currency, withdrawal_currency)
        return deposit_currency, withdrawal_currency


    def create_a_swap(self,
                      swap_pair = None,
                      withdrawal_address = None,
                      refund_address = "",
                      deposit_amount = 0,
                      user_id = "",
                      affiliate_margin = 5,
                      affiliate_payment_address = "1fs4Vz12WGBgPe6LmE2TDnGeuAjFhws6k",
                      url = "/api/v2/public/swap",
                      debug = False):
        '''
        Returns:
            {"swap_id":"e8555143-124e-4103-8c61-7394b7203622","created_at":"2018-09-13T08:22:06.710Z","user_id":"","deposit_address":"3FozwEKNCxCxQ2H1drh3P9WdEvPFcbGZAj","deposit_currency":"BTC","withdrawal_address":"0x08d62881d04f62a02ee80f45abf454f418c60e99","withdrawal_currency":"ETH","refund_address":"0x08d62881d04f62a02ee80f45abf454f418c60e99","affiliate_margin":5,"affiliate_payment_address":"1fs4Vz12WGBgPe6LmE2TDnGeuAjFhws6k","status":"awaiting deposit"}'
        '''

        if debug:
            withdrawal_address = "0x08d62881d04f62a02ee80f45abf454f418c60e99"
            swap_pair = "BTC_ETH"
            refund_address = "0x08d62881d04f62a02ee80f45abf454f418c60e99"

        if withdrawal_address is None:
            raise errors.RequestError("withdrawal_address missing.")

        if swap_pair is None:
            raise errors.RequestError("Swap pair is missing. eg: BTC_ETH for BTC deposit, ETh withdrawal")

        deposit_currency, withdrawal_currency = swap_pair.split("_")

        data = {}
        data["deposit_currency"] = deposit_currency
        data["withdrawal_currency"] = withdrawal_currency
        data["withdrawal_address"] = withdrawal_address
        data["refund_address"] = refund_address
        data["deposit_amount"] = deposit_amount
        data["user_id"] = user_id
        data["affiliate_margin"] = affiliate_margin
        data["affiliate_payment_address"] = affiliate_payment_address


        if debug:
            print ("Post Arg: %s" %data )

        req = self._request("post", url, data=data, debug=debug)

        if debug:
            print (req)
        return req



    def get_supported_currencies(self, url = "/api/v2/public/currencies"):
        return self._request("GET", url)


    def _get(self, url):
        return self._request("get", url)

    def _post(self, url, data={}):
        return self._request("post", url, data=data)

    def _delete(self, url):
        return self._request("delete", url)

    def updates(self, since):
        return self._post("/updates", {"last_activity_date": since} if since else {})

    def meta(self):
        return self._get("/meta")

    def add_profile_photo(self, fbid, x_dist, y_dist, x_offset, y_offset):
        data = {
                "transmit": "fb",
                "assets": [{"id": str(fbid), "xdistance_percent": float(x_dist), "ydistance_percent": float(y_dist),
                            "xoffset_percent": float(x_offset), "yoffset_percent": float(y_offset)}]
               }

        return self._request("post", constants.CONTENT_BASE + "/media", data=data)

    def delete_profile_photo(self, photo_id):
        data = {"assets": [photo_id]}

        return self._request("delete", constants.CONTENT_BASE + "/media", data=data)

    def recs(self, limit=10):
        return self._post("/user/recs", data={"limit": limit})

    def matches(self, since):
        return self.updates(since)['matches']

    def profile(self):
        return self._get("/profile")

    def update_profile(self, profile):
        return self._post("/profile", profile)

    def like(self, user):
        return self._get("/like/{}".format(user))

    def dislike(self, user):
        return self._get("/pass/{}".format(user))

    def message(self, user, body):
        return self._post("/user/matches/{}".format(user),
                          {"message": str(body)})

    def message_gif(self, user, giphy_id):
        return self._post("/user/matches/{}".format(user),
                          {"type": "gif", "gif_id": str(giphy_id)})

    # def report(self, user, cause=constants.ReportCause.Other, text=""):
    #     try:
    #         cause = int(cause)
    #     except TypeError:
    #         cause = int(cause.value)
    #
    #     data = {"cause": cause}
    #
    #     if text and constants.ReportCause(cause) == constants.ReportCause.Other:
    #         data["text"] = text
    #
    #     return self._post("/report/" + user, data)

    def user_info(self, user_id):
        return self._get("/user/" + user_id)

    def ping(self, lat, lon):
        return self._post("/user/ping", {"lat": lat, "lon": lon})

    def share(self, user):
        return self._post("/user/{}/share".format(user))

    def superlike(self, user):
        result = self._post("/like/{}/super".format(user))
        if 'limit_exceeded' in result and result['limit_exceeded']:
            raise errors.RequestError("Superlike limit exceeded")
        return result

    def fb_friends(self):
        """
        Requests records of all facebook friends using Tinder Social.
        :return: object containing array of all friends who use Tinder Social.
        """
        return self._get("/group/friends")

    def like_message(self, message):
        """
        Hearts a message sent by a match
        :param message: message id
        :return: empty json, response code is 201 (Created)
        """
        return self._post("/message/{}/like".format(message.id))

    def unlike_message(self, message):
        """
        Removes heart from a message
        :param message: message id
        :return: empty json, response code is 204 (No content)
        """
        return self._delete("/message/{}/like".format(message.id))

    def liked_messages(self, since):
        return self.updates(since)['liked_messages']