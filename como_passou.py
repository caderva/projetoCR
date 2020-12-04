def como_passou(prior, likelihood, mode):

    prior_A = float(prior[0])
    prior_B = float(prior[1])
    prior_C = float(prior[2])
    prior_D = float(prior[3])
    prior_F = float(prior[4])

    # Likelihoods
    lk_A = float(likelihood[0])
    lk_B = float(likelihood[1])
    lk_C = float(likelihood[2])
    lk_D = float(likelihood[3])
    lk_F = float(likelihood[4])

    # Posterior Results
    results = []

    a = prior_F * lk_F
    b = prior_D * lk_D
    c = prior_C * lk_C
    d = prior_B * lk_B
    f = prior_A * lk_A

    p = a + b + c + d + f

    results.append((prior_F * lk_F) / p)
    results.append((prior_D * lk_D) / p)
    results.append((prior_C * lk_C) / p)
    results.append((prior_B * lk_B) / p)
    results.append((prior_A * lk_A) / p)

    mean = 0 * results[0] + 1 * results[1] + 2 * results[2] + 3 * results[3] + 4 * results[4]

    if mode == 1:
        return round(mean)
    else:
        return results.index(max(results))


# CODIGO ANTIGO (VAI QUE O PRIMEIRO DA PAU)

# prior = [0.2, 0.3, 0.25, 0.15, 0.1]
# likelihood = [0.1, 0.15, 0.15, 0.25, 0.35]


# prior_A = float(prior[0])
    # prior_B = float(prior[1])
    # prior_C = float(prior[2])
    # prior_D = float(prior[3])
    # prior_F = float(prior[4])
    #
    # # Likelihoods
    # lk_A = float(likelihood[0])
    # lk_B = float(likelihood[1])
    # lk_C = float(likelihood[2])
    # lk_D = float(likelihood[3])
    # lk_F = float(likelihood[4])
    #
    # # Posterior Results
    # results = []
    #
    # results.append(prior_F * lk_F)
    # results.append(prior_D * lk_D)
    # results.append(prior_C * lk_C)
    # results.append(prior_B * lk_B)
    # results.append(prior_A * lk_A)
    #
    # return results.index(max(results)

