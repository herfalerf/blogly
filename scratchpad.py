 user = User.query.get_or_404(user_id)
    title = request.form["title"]
    content = request.form["content"]
    user = user_id
    new_post = Post(title=title, content=content, user_id=user)

    db.session.add(new_post)
    db.session.commit()