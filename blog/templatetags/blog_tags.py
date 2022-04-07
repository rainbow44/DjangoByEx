import markdown
from django import template
from django.db.models import Count
from django.utils.safestring import mark_safe

from ..models import Post

register = template.Library()


@register.simple_tag  # simple_tag - processes the data and returns a string
def total_posts():
    return Post.published.count()


@register.inclusion_tag('blog/post/latest_posts.html')  # inclusion_tag-processes the data. returns a rendered template
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}


@register.simple_tag  # simple tag with a stored variable
def get_most_commented_posts(count=5):
    return Post.published.annotate(
        total_comments=Count('comments')).order_by('-total_comments')[:count]


@register.filter(name='markdown')  # template filter
def markdown_format(text):
    return mark_safe(markdown.markdown(text))
