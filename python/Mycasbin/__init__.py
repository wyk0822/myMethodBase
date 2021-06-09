import casbin
import casbin_sqlalchemy_adapter
import casbin
import flask
adapter = casbin_sqlalchemy_adapter.Adapter('sqlite:///test.db')

e = casbin.Enforcer('model.conf', adapter)

sub = "alice"  # the user that wants to access a resource.
obj = "data1"  # the resource that is going to be accessed.
act = "read"  # the operation that the user performs on the resource.

# print(e.add_policy(sub, obj, act)) # 添加字段

print(e.get_adapter())

if e.enforce(sub, obj, act):
    # permit alice to read data1casbin_sqlalchemy_adapter
    print(f"允许{sub}读取{obj}")
else:
    # deny the request, show an error
    print("拒绝请求，抛出异常")

# e = casbin.Enforcer("model.conf", "policy.csv")
#
# sub = "zhangsan"  # 想要访问资源的用户
# obj = "testData"  # 将要被访问的资源
# act = "read"  # 用户对资源进行的操作
#
# if e.enforce(sub, obj, act):
#     # 允许alice读取data1
#     print(f"允许{sub}读取{obj}")
# else:
#     # 拒绝请求，抛出异常
#     print("拒绝请求，抛出异常")
# s = e.add_policy("test", "d", "1")
# print(s)