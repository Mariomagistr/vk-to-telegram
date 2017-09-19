import vk_api as vk
import telegram_api as telegram 
import time
import config
import attachments

visited_posts = []

def load_visited_posts():
    try:
        f = open('data.txt', 'r', encoding = 'utf-8')
        visited_posts = []
        counter = 0
        for line in f:
            visited_posts.append(int(line[:-1]))
        return visited_posts
    except:
        return []
    
def dump_visited_posts(visited_posts):
    f = open('data.txt', 'w', encoding = 'utf-8')
    for i in visited_posts:
        f.write(str(i) + '\n')
        

def something_new(visited_posts):
    data = vk.vkMethod('wall.get', {'domain': config.vkPublic, 'count': 2})
    time.sleep(0.5)
    if(data['items'][1]['id'] in visited_posts):
        return False
    else:
        return True
    
def get_group_name(id):
    data = vk.vkMethod('groups.getById', {'group_ids': str(-id) + ','})
    return data[0]['name']
    
def get_screen_name(id):
    data = vk.vkMethod('groups.getById', {'group_ids': str(-id) + ','})
    print(data)
    time.sleep(0.5)
    return data[0]['screen_name']
    
def link_by_attach(attach, owner_id):
        if attach['type'] == 'video':
            real_shit_owner_id = attach['owner_id']
            return 'https://vk.com/{}?z=video{}_{}'.format(get_screen_name(owner_id), real_shit_owner_id, attach['id'])
        if attach['type'] == 'photo':
            print(attach)
            maxsize = 0
            for i in attach:
                if 'photo' in i:
                    maxsize = max(maxsize, int(i.split('_')[-1]))
            return attach['photo_{}'.format(str(maxsize))]
        return ''
    
def send_message_by_attach(attach, owner_id, rep):
    text = ''
    if rep:
        text += '{}{}\n\n'.format('\U000021AA ' * rep, get_group_name(owner_id))
    text += link_by_attach(attach, owner_id)
    telegram.TMethod('sendMessage', {'chat_id': config.TChannel, 'parse-mod': 'HTML', 'text': text})
    time.sleep(0.5)

def send_message_by_post(post, rep = 0):
    if not 'attachments' in post:
        post['attachments'] = []
    for i in range(len(post['attachments'])):
        type = post['attachments'][i]['type']
        post['attachments'][i] = post['attachments'][i][type]
        post['attachments'][i]['type'] = type
    attachs = []
    text = ''
    if rep:
        text += '{} {}\n\n'.format('\U000021AA' * rep, get_group_name(post['owner_id']))
    text += post['text']
    if len(post['attachments']):
        text += '\n\n{}'.format(link_by_attach(post['attachments'][0], post['owner_id']))
    if(len(text) or len(post['attachments'])):
        if '[id' in text:
            left1 = text.find('[id')
            left2 = text.find('|', left1)
            i = left2 + 1
            while text[i] != ']':
                i += 1
            text = text[:left1] + text[left2 + 1:i] + text[i + 1:]
        telegram.TMethod('sendMessage', {'chat_id': config.TChannel, 'parse-mod': 'HTML', 'text': text})
    time.sleep(0.5)
    print(post['attachments'])
    if 'copy_history' in post:
        print(12)
        send_message_by_post(post['copy_history'][0], rep + 1)
    for i in range(1, len(post['attachments'])):
        send_message_by_attach(post['attachments'][i], rep)
    return post['id']
        
def get_new_posts(visited_posts):
    posts = []
    offset = 1
    post = vk.vkMethod('wall.get', {'domain': config.vkPublic, 'offset': offset, 'count': 1})['items'][0]
    time.sleep(0.5)
    while post['id'] not in visited_posts:
        posts.append(post)
        offset += 1
        post = vk.vkMethod('wall.get', {'domain': config.vkPublic, 'offset': offset, 'count': 1})['items'][0]
        time.sleep(0.5)
        if offset > 10:
            break
    return posts
        

# main loop
while True:
    visited_posts = load_visited_posts()
    pinned_post = vk.vkMethod('wall.get', {'domain': config.vkPublic, 'count': 1})['items'][0]
    if pinned_post['id'] not in visited_posts:
        visited_posts.append(send_message_by_post(pinned_post))
    if something_new(visited_posts):
        posts = get_new_posts(visited_posts)
        for i in range(len(posts) -1, -1, -1):
            visited_posts.append(send_message_by_post(posts[i]))
        dump_visited_posts(visited_posts)
    else:
        print('nothing new, sir')
        time.sleep(60)
