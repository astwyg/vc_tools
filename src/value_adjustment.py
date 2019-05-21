import matplotlib.pyplot as plt

def method_gyz(x):
    if x > 18000:
        return 0
    else:
        return (2500/(x*0.8)-17.24/100)*(2.1/2.4)

def method_hqg(x):
    if x > 18000:
        return 0
    else:
        return ((18000-x)/(18000-14500))*(17.24/100-15.09/100)

def method_wyg(x):
    if x > 18000:
        return 0
    else:
        return (3000/(x+3000)-12.5/100) - (3000/21000-12.5/100)

def method_hupo(x):
    return (3000/(x+3000)-3000/24000)

def get_new_value():
    return list(range(21000,14500,-1))

if __name__ == "__main__":

    hupo_compensate = []
    method_gyz_compesate = []
    method_hqg_compesate = []
    method_wyg_compesate = []
    for x in get_new_value():
        hupo_compensate.append(method_hupo(x))
        method_gyz_compesate.append(method_gyz(x))
        method_hqg_compesate.append(method_hqg(x))
        method_wyg_compesate.append(method_wyg(x))

    plt.plot(get_new_value(), hupo_compensate, label="hupo_compensate")
    plt.plot(get_new_value(), method_gyz_compesate, label="method_gyz_compesate")
    plt.plot(get_new_value(), method_hqg_compesate, label="method_hqg_compesate")
    plt.plot(get_new_value(), method_wyg_compesate, label="method_wyg_compesate")
    plt.legend(loc='upper right')

    plt.show()
