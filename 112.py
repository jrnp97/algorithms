#       mov = [None, 0, 1] 50%
#    expect = [None, 0, 1, 1, 0, 1]
# ideal = [None, 0, 1, 1, 0]  # 90% patterns


def is_bouncy(move):
    return move.count(0) > 0 and move.count(1) > 0


def get_moviment(number):
    moviment = [None]
    for i in range(len(number) - 1):
        if number[i] >= number[i + 1]:
            moviment.append(0)
        else:
            moviment.append(1)
    return moviment


def check(initial):
    num_list = [int(val) for val in str(initial)]
    patron = get_moviment(num_list)
    done = is_bouncy(patron)
    return patron, done


if __name__ == "__main__":

    initial = 100
    count = 1
    cant = 1
    num_list = [int(val) for val in str(initial)]
    patron = get_moviment(num_list)
    while count < 1000:
        patt, done = check(initial)
        print(f"Numero {initial} "
              f"| patron -> {patron} "
              f"| is_bouncy = {done} "
              f"| {cant if done else None}")
        if done:
            cant += 1
        initial += 1
        count += 1

    print(cant)
