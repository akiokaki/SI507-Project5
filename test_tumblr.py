import pytumblr
import secret_data_tumblr
import json
import csv
from datetime import datetime

CLIENT_KEY = secret_data_tumblr.client_key 
CLIENT_SECRET = secret_data_tumblr.client_secret 
OAUTH_TOKEN = secret_data_tumblr.oauth_token
OAUTH_SECRET = secret_data_tumblr.oauth_secret

client = pytumblr.TumblrRestClient(CLIENT_KEY, CLIENT_SECRET, OAUTH_TOKEN, OAUTH_SECRET)


#########################
##### CACHING SETUP #####
#########################
#--------------------------------------------------
# Caching constants
#--------------------------------------------------

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S.%f"
DEBUG = True
CACHE_FNAME = "cache_contents.json"
CREDS_CACHE_FILE = "creds.json"

#--------------------------------------------------
# Load cache files: data and credentials
#--------------------------------------------------
# Load data cache
try:
    with open(CACHE_FNAME, 'r') as cache_file:
        cache_json = cache_file.read()
        CACHE_DICTION = json.loads(cache_json)
except:
    CACHE_DICTION = {}


#---------------------------------------------
# Cache functions
#---------------------------------------------
def has_cache_expired(timestamp_str, expire_in_days):
    """Check if cache timestamp is over expire_in_days old"""
    # gives current datetime
    now = datetime.now()

    # datetime.strptime converts a formatted string into datetime object
    cache_timestamp = datetime.strptime(timestamp_str, DATETIME_FORMAT)

    # subtracting two datetime objects gives you a timedelta object
    delta = now - cache_timestamp
    delta_in_days = delta.days


    # now that we have days as integers, we can just use comparison
    # and decide if cache has expired or not
    if delta_in_days > expire_in_days:
        return True # It's been longer than expiry time
    else:
        return False

def get_from_cache(identifier, dictionary):
    """If unique identifier exists in specified cache dictionary and has not expired, return the data associated with it from the request, else return None"""
    identifier = identifier.upper() # Assuming none will differ with case sensitivity here
    if identifier in dictionary:
        data_assoc_dict = dictionary[identifier]
        if has_cache_expired(data_assoc_dict['timestamp'],data_assoc_dict["expire_in_days"]):
            if DEBUG:
                print("Cache has expired for {}".format(identifier))
            # also remove old copy from cache
            del dictionary[identifier]
            data = None
        else:
            data = dictionary[identifier]['values']
    else:
        data = None
    return data

def set_in_data_cache(identifier, data, expire_in_days):
    """Add identifier and its associated values (literal data) to the data cache dictionary, and save the whole dictionary to a file as json"""
    identifier = identifier.upper()
    CACHE_DICTION[identifier] = {
        'values': data,
        'timestamp': datetime.now().strftime(DATETIME_FORMAT),
        'expire_in_days': expire_in_days
    }

    with open(CACHE_FNAME, 'w') as cache_file:
        cache_json = json.dumps(CACHE_DICTION)
        cache_file.write(cache_json)

def create_request_identifier(params_diction):
    sorted_params = sorted(params_diction.items(),key=lambda x:x[0])
    params_str = "/".join([str(e) for l in sorted_params for e in l]) # Make the list of tuples into a flat list using a complex list comprehension
    total_ident = params_str
    print(total_ident)
    return total_ident.upper() # Creating the identifier
        

if __name__ == "__main__":
    if not CLIENT_KEY or not CLIENT_SECRET:
        print("You need to fill in client_key and client_secret in the secret_data.py file.")
        exit()

    ############################
    ##### Make the request #####
    ############################

    dashboard_diction = {"tumblr":"dashboard"}
    
    dashboard_ident = create_request_identifier(dashboard_diction)
    data = get_from_cache(dashboard_ident, CACHE_DICTION)
    final_output_blog = []
    final_output_dashboard = []
    expire_in_days = 7
    
    if data:
        if DEBUG:
            print("Loading from data cache: {}... data".format(dashboard_ident))
    else:
        if DEBUG:
            print("Fetching new data")
        dashboard_stuff = client.dashboard(limit=10)
        with open('dashboard.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['date','id','post_url'])
            for i in dashboard_stuff['posts']:
                final_output_dashboard.append(i['date'])
                final_output_dashboard.append(str(i['id']))
                final_output_dashboard.append(i['post_url'])
            num_list = [0,3,6,9,12,15,18,21,24,27]
            for i in num_list:
                print(i)
                writer.writerow([final_output_dashboard[i],final_output_dashboard[i+1],final_output_dashboard[i+2]])
        set_in_data_cache(dashboard_ident, final_output_dashboard, expire_in_days)
                
    posts_diction = {"tumblr":"posts"}
    
    post_ident = create_request_identifier(posts_diction)
    data = get_from_cache(post_ident, CACHE_DICTION)
    if data:
        if DEBUG:
            print("Loading from data cache: {}... data".format(post_ident))
    else:
        if DEBUG:
            print("Fetching new data")
        blog_stuff = client.posts('hamansamabanzai.tumblr.com', limit=10)
        with open('post.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['date','id','post_url'])
            for i in blog_stuff['posts']:
                final_output_blog.append(i['date'])
                final_output_blog.append(str(i['id']))
                final_output_blog.append(i['post_url'])
            num_list = [0,3,6,9,12,15,18,21,24,27]
            for i in num_list:
                print(i)
                writer.writerow([final_output_blog[i],final_output_blog[i+1],final_output_blog[i+2]])
        set_in_data_cache(post_ident, final_output_blog, expire_in_days)
                
        # dashboard_stuff_str = ''.join('{}{}'.format(key, val) for key, val in dashboard_stuff.items())
        # data = json.loads(dashboard_stuff)
        # data2 = json.loads(blog_stuff)
        # set_in_data_cache(ident, data2, expire_in_days)
        
        # with open('dashboard.csv', 'w', newline='') as csvfile:
            # writer = csv.writer(csvfile)
            # writer.writerow(['date','id','post_url'])
            # i=0
            # while i<len(final_output_dashboard):
                # writer.writerow([final_output_dashboard[i:i+2]])
            # i+=3
            # number_of_items = 0
            # while number_of_items <= len(final_output_dashboard)/3:
                # i=0
                # while i<3:
                    # i+=1
            # number_of_items+=1


