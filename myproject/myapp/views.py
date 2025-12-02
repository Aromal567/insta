from django.shortcuts import render,redirect
from django.contrib.auth.models import *
from django.contrib import auth,messages
from . models import *

# Create your views here.
def login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        query1=Login.objects.filter(username=username,password=password).exists()
        if query1:
            query2=Login.objects.get(username=username,password=password)
            request.session["lid"]=query2.pk
            lid=request.session.get('lid')
            if query2.user_type=='admin':
                return redirect('adminhome')
            elif query2.user_type=='user':
                u=User.objects.get(LOGIN=lid)
                request.session["user_id"]=u.pk
                return redirect('home')
    return render(request,'login.html')       


def adminhome(request):
    return render(request,'adminhome.html')


def logout(request):
    return redirect('login')


def userregister(request):
    if request.method=='POST':
        username=request.POST['username']
        firstname=request.POST['firstname']
        lastname=request.POST['lastname']
        email=request.POST['email']
        phone=request.POST['phone']
        image = request.FILES.get('image')
        password=request.POST['password']

        q1=Login.objects.create(username=username,password=password,user_type='user')
        q1.save()

        q2=User.objects.create(firstname=firstname,lastname=lastname,email=email,phone=phone,image=image,LOGIN_id=q1.pk)
        q2.save()
        return redirect('login')
    return render(request,'userregister.html')


def home(request):
    post=Post.objects.all()
    reel=Reel.objects.all()
    return render(request,'home.html',{'result':post,'reel':reel})



def adminuserview(request):
    name=User.objects.all()
    return render(request,'adminuserview.html',{'result':name})

def adminreelview(request):
    name=Reel.objects.all()
    return render(request,'adminreelview.html',{'result':name})


def userdelete(request,id):
    User.objects.get(id=id).delete()
    return redirect('adminuserview')

def userblock(request,id):
    q=User.objects.get(id=id)
    userlogin=q.LOGIN.pk
    q2=Login.objects.get(id=userlogin)
    q2.user_type='blocked'
    q2.save()
    return redirect('adminuserview')

def userunblock(rquest,id):
    q=User.objects.get(id=id)
    userlogin=q.LOGIN.pk
    q2=Login.objects.get(id=userlogin)
    q2.user_type='user'
    q2.save()
    return redirect('adminuserview')


def post_create(request):
    user_id=request.session["user_id"]
    if request.method == 'POST':
        image = request.FILES.get('image')
        description = request.POST['description']

        post=Post.objects.create(image=image,description=description,USER_id=user_id,like_count=0)
        post.save()
        
        return redirect('home')
    return render(request,'post_create.html')



def reel_create(request):
    user_id=request.session["user_id"]
    if request.method=='POST':
        video = request.FILES['video']
        caption=request.POST['caption']
        reel=Reel.objects.create(video=video,caption=caption,USER_id=user_id)
        reel.save()
        return redirect('home')
    return render(request,'reel_create.html')


def reel_view(request):
    reel=Reel.objects.all()
    return render(request,'reel_view.html',{'result':reel})





def mypost(request):
    user_id= request.session["user_id"]
    name=Post.objects.filter(USER_id=user_id)
    reel=Reel.objects.filter(USER_id=user_id)
    return render(request,'mypost.html',{'result':name,'reel':reel})


def adminpostview(request):
    name=Post.objects.all()
    return render(request,'adminpostview.html',{'result':name})



def admindltpost(request,id):
    Post.objects.get(id=id).delete()
    return redirect('adminpostview')

def mypostdlt(request,id):
    Post.objects.get(id=id).delete()
    return redirect('mypost')


def reeldlt(request,id):
    Reel.objects.get(id=id).delete()
    return redirect('mypost')


def comment(request,id):
    post_id=id
    user_id=request.session["user_id"]
    if request.method == 'POST':
        date_time = request.FILES.get('date_time')
        comment = request.POST['comment']

        cmt2=Comments.objects.create(date_time=date_time,comment=comment,POST_id=post_id,USER_id=user_id)
        cmt2.save()
        return redirect('home')
    return render(request,'comment.html',{'post_id':post_id})



def reel_cmt(request,id):
    reel_id=id
    user_id=request.session["user_id"]
    if request.method=='POST':
        date_time=request.FILES.get('date_time')
        comment=request.POST['comment']

        cmt=Rcomment.objects.create(date_time=date_time,comment=comment,REEL_id=reel_id,USER_id=user_id)
        cmt.save()
    return render(request,'reel_cmt.html',{'reel_id':reel_id})


def reelcmtview(request,id):
    comment=Rcomment.objects.filter(REEL_id=id)
    return render(request,'reelcmtview.html',{'result':comment})


def usercmtview(request,id):
    comments = Comments.objects.filter(POST_id=id)  
    return render(request, 'usercmtview.html', {'result': comments})



def mypostedit(request,id):
    old_data=Post.objects.get(id=id)
    if request.method=='POST':
        image = request.FILES.get('image')
        description = request.POST['description']

        old_data.description=description
        if image:
            old_data.image=image
        old_data.save()  
        return redirect('home')
    return render(request,'mypostedit.html',{'result':old_data})



def reeledit(request,id):
    old_reel=Reel.objects.get(id=id)
    if request.method=='POST':
        video=request.FILES.get('video')
        caption=request.POST['caption']

        old_reel.caption=caption
        if video:
            old_reel.video=video
        old_reel.save()    
        return redirect('home')
    return render(request,'reeledit.html',{'result':old_reel})




# def like(request,id):
#     post_id=id
#     user_id=request.session["user_id"]
#     q1=Post.objects.get(id=post_id)
#     q1.like_count += 1 
#     q1.save()

#     like=Likes.objects.create(USER_id=user_id,POST_id=post_id)
#     like.save()
#     return redirect('home')


def like(request, id):
    post_id = id
    user_id = request.session["user_id"]

    # Only like if not already liked
    if not Likes.objects.filter(USER_id=user_id, POST_id=post_id).exists():
        post = Post.objects.get(id=post_id)
        post.like_count += 1
        post.save()

        Likes.objects.create(USER_id=user_id, POST_id=post_id)
    return redirect('home')



def reel_like(request, id):
    reel_id = id
    user_id = request.session["user_id"]

    if not Rlike.objects.filter(USER_id=user_id, REEL_id=reel_id).exists():
        reel = Reel.objects.get(id=reel_id)
        reel.like_count += 1
        reel.save()
        Rlike.objects.create(USER_id=user_id, REEL_id=reel_id)

    return redirect('reel_view')



def mylikeview(request,id):
    like=Likes.objects.filter(POST_id=id)
    return render(request,'mylikeview.html',{'result':like})



def reel_like_view(request,id):
    reel=Rlike.objects.filter(REEL_id=id)
    return render(request,'reel_like_view.html',{'result':reel})


# def view_other_users(request):
#     q=User.objects.exclude(id=request.session["user_id"])
#     q2=Friends.objects.filter(USER_1_id=request.session["user_id"])
#     requested_user_ids = q2.values_list('USER_2_id', flat=True)
#     return render(request,'viewotherview.html',{'result':q,'requested_user_ids':requested_user_ids})




# def view_other_users(request):
#     user_id = request.session["user_id"]
#     users = User.objects.exclude(id=user_id)
#     requested_user_ids = Friends.objects.filter(USER_1_id=user_id, status='pending' ).values_list('USER_2_id', flat=True)
       
#     friend_user_ids = Friends.objects.filter(USER_1_id=user_id, status='friends').values_list('USER_2_id', flat=True)
        
#     pending_request_user_ids = Friends.objects.filter(USER_2_id=user_id, status='pending').values_list('USER_1_id', flat=True)
#     return render(request, 'viewotherview.html',{'result': users,'requested_user_ids': requested_user_ids,'friend_user_ids': friend_user_ids,'pending_request_user_ids': pending_request_user_ids})




def view_other_users(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect('login')  

    if request.method == "POST":
        unfollow_id = request.POST.get("unfollow_id")
        if unfollow_id:
            Friends.objects.filter(
                USER_1_id=user_id, USER_2_id=unfollow_id, status='friends'
            ).delete()
            Friends.objects.filter(
                USER_1_id=unfollow_id, USER_2_id=user_id, status='friends'
            ).delete()
            return redirect('view_other_users')
    users = User.objects.exclude(id=user_id)
    requested_user_ids = Friends.objects.filter(
        USER_1_id=user_id, status='pending'
    ).values_list('USER_2_id', flat=True)

    friend_user_ids = Friends.objects.filter(
        USER_1_id=user_id, status='friends'
    ).values_list('USER_2_id', flat=True)

    pending_request_user_ids = Friends.objects.filter(
        USER_2_id=user_id, status='pending'
    ).values_list('USER_1_id', flat=True)

    return render(request, 'viewotherview.html', {
        'result': users,
        'requested_user_ids': requested_user_ids,
        'friend_user_ids': friend_user_ids,
        'pending_request_user_ids': pending_request_user_ids,
    })




def followrequest(request,id):
    user_1_id=request.session["user_id"]
    user_2_id=id
    friend=Friends.objects.create(USER_1_id=user_1_id,USER_2_id=user_2_id,status="pending")
    friend.save()
    return redirect('view_other_users')



def follow(request):
    follow=Friends.objects.filter(USER_2_id=request.session["user_id"])
    return render(request,'follow.html',{'result':follow})


def followback(request,id):
    q1=Friends.objects.get(id=id)
    q1.status='friends'
    q1.save()
    return redirect('follow')


def myfollowers(request):
    user_id = request.session["user_id"]
    friends = Friends.objects.filter(USER_2_id=user_id,status='friends')
    return render(request,'myfollowers.html', {'result': friends})



# def sendmessage(request):
#     user_id=request.session["user_id"]
#     sender = User.objects.get(id=Sender_id)
#     receiver = User.objects.get(id=Reciever_id)
#     if request.method=='POST':
#         message=request.POST['message']
#         msg=Message.objects.create(message=message,USER_id=user_id)
#         msg.save()
#     return render(request,'sendmessage.html')



def sendmessage(request, receiver_id):
    sender_id = request.session.get("user_id")
    sender = User.objects.get(id=sender_id)
    receiver = User.objects.get(id=receiver_id)

    if request.method == 'POST':
        msg = request.POST.get('message')
        if msg:
            Message.objects.create(Sender=sender, Reciever=receiver, message=msg)
            return redirect('sendmessage', receiver_id=receiver.id)

    messages = Message.objects.filter(Sender__in=[sender, receiver], Reciever__in=[sender, receiver] ).order_by('date_time')

    return render(request, 'sendmessage.html', {'messages': messages, 'receiver': receiver})



def usermsgview(request):
    user=User.objects.exclude(id=request.session["user_id"])
    return render(request,'usermsgview.html',{'result':user})

def adminmsgview(request):
    msg=Message.objects.all()
    return render(request,'adminmsgview.html',{'result':msg})