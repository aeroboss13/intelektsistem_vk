import vk_api
import networkx as nx


def group_users_friends_of_friends(user_id, users_id):
    G = nx.Graph()  # реализация простого неориентированного графа.

    for user in users_id:
        G.add_edge(user_id, user)  # значение для дуги

    return G


def group_users_friends(user_id, users_id):
    G = nx.Graph()

    for user in users_id:
        # G = nx.compose(G, group_users_friends_of_friends(user, session.get_api().friends.get(users_id = user)))
        G.add_edge(user_id, user)
    return G


def group_users(session):
    F = nx.Graph()

    with open("users.txt", "r") as file:
        for user in file.readlines():
            # F = nx.compose(F, group_users_friends(user.strip("\n"), session.get_api().friends.get(user_id=user.strip("\n"))["items"], session))
            F = nx.compose(F, group_users_friends(user.strip("\n"),
                                                  session.get_api().friends.get(user_id=user.strip("\n"))["items"]))
            # Составляем граф F с помощью G, объединив узлы и ребра в единый граф.
    return F


def autorization(login, password):
    vk_session = vk_api.VkApi(login=login, password=password)
    try:
        vk_session.auth(reauth=True)
    except vk_api.Captcha as cap:
        print(cap.get_url())
        cap.try_again(key=input())
    return vk_session


if __name__ == "__main__":
    from config import login, password

    group_user = group_users(autorization(login, password))
    print(nx.degree_centrality(group_user))
