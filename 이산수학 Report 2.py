"""Report 2: 관계행렬의 동치관계 판별과 폐포 구현."""

N = 5
A = [1, 2, 3, 4, 5]


def input_relation():
    relation = []
    print('집합 A = {1, 2, 3, 4, 5}')
    print('5×5 관계행렬을 한 행씩 입력하세요. 예: 1 0 0 0 0')
    for i in range(N):
        while True:
            try:
                row = list(map(int, input(f'{i+1}번째 행: ').split()))
                if len(row) != N or any(x not in (0, 1) for x in row):
                    print('0 또는 1을 정확히 5개 입력해주세요.')
                    continue
                relation.append(row)
                break
            except ValueError:
                print('정수 0과 1만 입력해주세요.')
    return relation


def print_matrix(relation):
    print('    1 2 3 4 5')
    for i, row in enumerate(relation, 1):
        print(f'{i} | ' + ' '.join(map(str, row)))


def print_ordered_pairs(relation):
    pairs = [(i+1, j+1) for i in range(N) for j in range(N) if relation[i][j]]
    print('R = {' + ', '.join(map(str, pairs)) + '}' if pairs else 'R = ∅')


def is_reflexive(relation):
    return all(relation[i][i] == 1 for i in range(N))


def is_symmetric(relation):
    return all(relation[i][j] == relation[j][i]
               for i in range(N) for j in range(N))


def is_transitive(relation):
    return all(not (relation[i][j] and relation[j][k]) or relation[i][k]
               for i in range(N) for j in range(N) for k in range(N))


def check_properties(relation):
    p = (is_reflexive(relation), is_symmetric(relation), is_transitive(relation))
    print('\n[관계 성질 판별]')
    for label, result in zip(('반사', '대칭', '추이'), p):
        print(f'{label}: ' + ('O' if result else 'X'))
    equivalent = all(p)
    print('동치관계: ' + ('O' if equivalent else 'X'))
    return equivalent


def print_counterexamples(relation):
    print('\n[추가기능: 성질별 반례]')
    if not is_reflexive(relation):
        i = next(i for i in range(N) if relation[i][i] == 0)
        print(f'반사성: ({i+1}, {i+1})이 없음')
    if not is_symmetric(relation):
        i, j = next((i, j) for i in range(N) for j in range(N)
                    if relation[i][j] and not relation[j][i])
        print(f'대칭성: ({i+1}, {j+1})은 있지만 ({j+1}, {i+1})은 없음')
    if not is_transitive(relation):
        i, j, k = next((i, j, k) for i in range(N) for j in range(N)
                       for k in range(N)
                       if relation[i][j] and relation[j][k] and not relation[i][k])
        print(f'추이성: ({i+1}, {j+1}), ({j+1}, {k+1})은 있지만 ({i+1}, {k+1})은 없음')


def print_equivalence_classes(relation):
    print('\n[각 원소의 동치류]')
    classes = []
    for i in range(N):
        current = tuple(j + 1 for j in range(N) if relation[i][j])
        print(f'[{i+1}] = ' + '{' + ', '.join(map(str, current)) + '}')
        if current not in classes:
            classes.append(current)
    print('\n[추가기능: 중복 제거한 집합의 분할]')
    print('{' + ', '.join('{' + ', '.join(map(str, c)) + '}' for c in classes) + '}')


def reflexive_closure(relation):
    closure = [row[:] for row in relation]
    for i in range(N):
        closure[i][i] = 1
    return closure


def symmetric_closure(relation):
    closure = [row[:] for row in relation]
    for i in range(N):
        for j in range(N):
            if closure[i][j] == 1:
                closure[j][i] = 1
    return closure


def transitive_closure(relation):
    closure = [row[:] for row in relation]
    for k in range(N):
        for i in range(N):
            for j in range(N):
                if closure[i][k] and closure[k][j]:
                    closure[i][j] = 1
    return closure


def make_equivalence_closure(relation):
    current = [row[:] for row in relation]
    for label, predicate, operation in (
        ('반사 폐포', is_reflexive, reflexive_closure),
        ('대칭 폐포', is_symmetric, symmetric_closure),
        ('추이 폐포', is_transitive, transitive_closure),
    ):
        if not predicate(current):
            print(f'\n[{label} 변환 전]')
            print_matrix(current)
            current = operation(current)
            print(f'[{label} 변환 후]')
            print_matrix(current)
        else:
            print(f'\n[{label}] 이미 성립하여 변환 생략')
    return current


def main():
    print('=== Report 2: 동치관계 판별 프로그램 ===')
    relation = input_relation()
    print('\n[입력한 관계행렬]')
    print_matrix(relation)
    print_ordered_pairs(relation)
    if check_properties(relation):
        print_equivalence_classes(relation)
    else:
        print_counterexamples(relation)
        final_relation = make_equivalence_closure(relation)
        print('\n[폐포 변환 후 최종 판별]')
        if check_properties(final_relation):
            print_equivalence_classes(final_relation)
        else:
            print('오류: 최종 동치관계가 완성되지 않았습니다.')


if __name__ == '__main__':
    main()
