from django.http import HttpResponse
import requests

# 認証が終わればInstagramからリダイレクトされるURL
def instagram_callback(request):
    # Instagramから送られてきた認証コードを取得
    code = request.GET.get('code')
    # コードがない場合はエラーを返す
    if not code:
        return HttpResponse("Error: Missing authorization code", status=400)
    
    # Instagram APIへアクセストークンをリクエスト
    token_url = "https://api.instagram.com/oauth/access_token"
    data = {
        # 'client_id': 'example',  # InstagramのクライアントID
        'client_id': 'XXXXXXXXXXXXXXXX',
        # 'client_secret': '9415796d4e66c9db07487d873a1b3602',  # Instagramのクライアントシークレット
        'client_secret': 'XXXXXXXXXXXXXXXX',
        'grant_type': 'authorization_code', #クライアントがどのようにしてアクセストークンを取得するかを指定するためのパラメータ
        'redirect_uri': 'https://example.onrender.com/accounts/auth/',  # このバックエンドのURL
        'code': code  # 取得した認証コード
    }
    
    # POSTリクエストでアクセストークンを取得
    response = requests.post(token_url, data=data)
    
    # アクセストークンが取得できた場合は、JavaScriptを使ってカスタムスキームのURLにリダイレクト
    if response.status_code == 200:
        token_data = response.json()
        access_token = token_data.get('access_token')
        
        # JavaScriptを使ってカスタムスキームのURLにリダイレクト
        redirect_url = f"example?access_token={access_token}"
        return HttpResponse(f"""
            <html>
                <head>
                    <script type="text/javascript">
                        window.location.href = "{redirect_url}";
                    </script>
                </head>
                <body>
                    Redirecting...
                </body>
            </html>
        """)
    else:
        # アクセストークンが取得できなかった場合はエラーを返す
        return HttpResponse("Error: Failed to retrieve access token", status=400)

