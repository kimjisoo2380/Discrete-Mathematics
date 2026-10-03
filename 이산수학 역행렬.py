EPS = 1e-10


# =========================================================
# 행렬 출력 함수
# =========================================================
def print_matrix(matrix):
    for row in matrix:
        for value in row:
            # -0.0000이 출력되는 것을 방지
            if abs(value) < EPS:
                value = 0

            print(f"{value:10.4f}", end=" ")

        print()


# =========================================================
# 특정 행과 열을 제거하여 소행렬 생성
# =========================================================
def get_minor(matrix, row, col):
    minor = []

    for i in range(len(matrix)):

        if i == row:
            continue

        new_row = []

        for j in range(len(matrix)):

            if j == col:
                continue

            new_row.append(matrix[i][j])

        minor.append(new_row)

    return minor


# =========================================================
# 행렬식 계산 함수
# =========================================================
def determinant(matrix):
    n = len(matrix)

    # 1 x 1 행렬
    if n == 1:
        return matrix[0][0]

    # 2 x 2 행렬
    if n == 2:
        return (
            matrix[0][0] * matrix[1][1]
            - matrix[0][1] * matrix[1][0]
        )

    # 3 x 3 이상
    # 첫 번째 행을 기준으로 여인수 전개
    det = 0

    for col in range(n):

        minor = get_minor(matrix, 0, col)

        det += (
            ((-1) ** col)
            * matrix[0][col]
            * determinant(minor)
        )

    return det


# =========================================================
# 행렬식 계산 과정 출력
# =========================================================
def print_determinant_process(matrix):
    n = len(matrix)

    print("\n[행렬식 계산 과정]")

    # 1 x 1
    if n == 1:

        print(f"det(A) = {matrix[0][0]:.4f}")
        return

    # 2 x 2
    if n == 2:

        a = matrix[0][0]
        b = matrix[0][1]
        c = matrix[1][0]
        d = matrix[1][1]

        result = a * d - b * c

        print(
            f"det(A) = "
            f"({a:.4f} × {d:.4f}) "
            f"- ({b:.4f} × {c:.4f})"
        )

        print(
            f"       = "
            f"{a * d:.4f} - {b * c:.4f}"
        )

        print(f"       = {result:.4f}")

        return

    # 3 x 3 이상
    print("첫 번째 행을 기준으로 여인수 전개합니다.\n")

    total = 0

    for col in range(n):

        minor = get_minor(matrix, 0, col)

        minor_det = determinant(minor)

        sign = 1 if col % 2 == 0 else -1

        term = (
            sign
            * matrix[0][col]
            * minor_det
        )

        print(
            f"항 {col + 1}: "
            f"({sign:+d}) × "
            f"{matrix[0][col]:.4f} × "
            f"det(M1{col + 1})"
        )

        print(
            f"        det(M1{col + 1}) "
            f"= {minor_det:.4f}"
        )

        print(
            f"        계산값 = {term:.4f}\n"
        )

        total += term

    print(f"det(A) = {total:.4f}")


# =========================================================
# 행렬식을 이용한 역행렬 계산
# =========================================================
def inverse_by_determinant(matrix):
    n = len(matrix)

    print(
        "\n========== "
        "행렬식을 이용한 역행렬 계산 "
        "=========="
    )

    # 행렬식 계산 과정 출력
    print_determinant_process(matrix)

    det = determinant(matrix)

    print(f"\n행렬식 det(A) = {det:.4f}")

    # 행렬식이 0이면 역행렬이 존재하지 않음
    if abs(det) < EPS:

        print(
            "[오류] 행렬식이 0이므로 "
            "역행렬이 존재하지 않습니다."
        )

        return None

    # 1 x 1 행렬
    if n == 1:

        inverse = [
            [1 / matrix[0][0]]
        ]

        print("\n[역행렬]")
        print_matrix(inverse)

        return inverse

    # -----------------------------------------------------
    # 여인수 행렬 계산
    # -----------------------------------------------------
    cofactor = [
        [0.0] * n
        for _ in range(n)
    ]

    print("\n[여인수 계산]")

    for i in range(n):

        for j in range(n):

            minor = get_minor(
                matrix,
                i,
                j
            )

            minor_det = determinant(minor)

            sign = (
                1
                if (i + j) % 2 == 0
                else -1
            )

            cofactor[i][j] = (
                sign * minor_det
            )

            print(
                f"C{i + 1}{j + 1} "
                f"= ({sign:+d}) × "
                f"{minor_det:.4f} "
                f"= {cofactor[i][j]:.4f}"
            )

    print("\n[여인수 행렬]")
    print_matrix(cofactor)

    # -----------------------------------------------------
    # 수반행렬
    # 여인수 행렬의 전치행렬
    # -----------------------------------------------------
    adjugate = []

    for i in range(n):

        row = []

        for j in range(n):

            row.append(
                cofactor[j][i]
            )

        adjugate.append(row)

    print(
        "\n[수반 행렬 "
        "= 여인수 행렬의 전치]"
    )

    print_matrix(adjugate)

    # -----------------------------------------------------
    # 역행렬 계산
    # A^-1 = 1 / det(A) × adj(A)
    # -----------------------------------------------------
    inverse = []

    for i in range(n):

        row = []

        for j in range(n):

            row.append(
                adjugate[i][j] / det
            )

        inverse.append(row)

    print(
        f"\n[역행렬 = "
        f"(1 / {det:.4f}) "
        f"× 수반 행렬]"
    )

    print_matrix(inverse)

    return inverse


# =========================================================
# 확대행렬 출력 함수
# =========================================================
def print_augmented(matrix, n):

    for row in matrix:

        # 왼쪽 행렬 A
        for j in range(n):

            value = row[j]

            if abs(value) < EPS:
                value = 0

            print(
                f"{value:9.4f}",
                end=" "
            )

        print("|", end=" ")

        # 오른쪽 행렬
        for j in range(n, 2 * n):

            value = row[j]

            if abs(value) < EPS:
                value = 0

            print(
                f"{value:9.4f}",
                end=" "
            )

        print()


# =========================================================
# 가우스-조던 소거법을 이용한 역행렬 계산
# =========================================================
def inverse_by_gauss_jordan(matrix):
    n = len(matrix)

    # -----------------------------------------------------
    # 확대행렬 [A | I] 생성
    # -----------------------------------------------------
    augmented = []

    for i in range(n):

        row = []

        # 원래 행렬 A
        for j in range(n):

            row.append(
                float(matrix[i][j])
            )

        # 단위행렬 I
        for j in range(n):

            if i == j:
                row.append(1.0)

            else:
                row.append(0.0)

        augmented.append(row)

    print(
        "\n========== "
        "가우스-조던 소거법 "
        "=========="
    )

    print(
        "\n[초기 확대 행렬 A | I]"
    )

    print_augmented(
        augmented,
        n
    )

    step = 1

    # -----------------------------------------------------
    # 각 열을 기준으로 피벗 설정
    # -----------------------------------------------------
    for col in range(n):

        # -------------------------------------------------
        # 피벗이 0일 경우 행 교환
        # -------------------------------------------------
        if abs(
            augmented[col][col]
        ) < EPS:

            swap_row = None

            for row in range(
                col + 1,
                n
            ):

                if abs(
                    augmented[row][col]
                ) > EPS:

                    swap_row = row
                    break

            # 교환할 수 있는 행도 없으면
            # 역행렬이 존재하지 않음
            if swap_row is None:

                print(
                    "\n[오류] "
                    "피벗을 찾을 수 없으므로 "
                    "역행렬이 존재하지 않습니다."
                )

                return None

            augmented[col], augmented[swap_row] = (
                augmented[swap_row],
                augmented[col]
            )

            print(
                f"\n[Step {step}] "
                f"R{col + 1} "
                f"↔ "
                f"R{swap_row + 1}"
            )

            print_augmented(
                augmented,
                n
            )

            step += 1

        # -------------------------------------------------
        # 피벗을 1로 만들기
        # -------------------------------------------------
        pivot = augmented[col][col]

        if abs(
            pivot - 1.0
        ) > EPS:

            for j in range(2 * n):

                augmented[col][j] /= pivot

            print(
                f"\n[Step {step}] "
                f"R{col + 1} "
                f"← "
                f"R{col + 1} "
                f"/ {pivot:.4f}"
            )

            print_augmented(
                augmented,
                n
            )

            step += 1

        # -------------------------------------------------
        # 현재 피벗 열의 나머지 원소를 0으로 만들기
        # -------------------------------------------------
        for row in range(n):

            if row == col:
                continue

            factor = augmented[row][col]

            if abs(factor) > EPS:

                for j in range(2 * n):

                    augmented[row][j] -= (
                        factor
                        * augmented[col][j]
                    )

                # factor가 양수인 경우
                if factor > 0:

                    operation = (
                        f"R{row + 1} "
                        f"← "
                        f"R{row + 1} "
                        f"- "
                        f"{factor:.4f}"
                        f"R{col + 1}"
                    )

                # factor가 음수인 경우
                else:

                    operation = (
                        f"R{row + 1} "
                        f"← "
                        f"R{row + 1} "
                        f"+ "
                        f"{abs(factor):.4f}"
                        f"R{col + 1}"
                    )

                print(
                    f"\n[Step {step}] "
                    f"{operation}"
                )

                print_augmented(
                    augmented,
                    n
                )

                step += 1

    # -----------------------------------------------------
    # 오른쪽 부분을 역행렬로 저장
    # -----------------------------------------------------
    inverse = []

    for i in range(n):

        row = []

        for j in range(
            n,
            2 * n
        ):

            row.append(
                augmented[i][j]
            )

        inverse.append(row)

    print(
        "\n[가우스-조던 소거법으로 "
        "구한 역행렬]"
    )

    print_matrix(inverse)

    return inverse


# =========================================================
# 두 역행렬 비교
# =========================================================
def are_matrices_equal(
    matrix1,
    matrix2,
    tolerance=1e-9
):

    if (
        matrix1 is None
        or matrix2 is None
    ):
        return False

    n = len(matrix1)

    for i in range(n):

        for j in range(n):

            if abs(
                matrix1[i][j]
                - matrix2[i][j]
            ) > tolerance:

                return False

    return True


# =========================================================
# 메인 프로그램
# =========================================================
def main():

    print(
        "===== 역행렬 계산 프로그램 ====="
    )

    # -----------------------------------------------------
    # 행렬 크기 입력
    # -----------------------------------------------------
    while True:

        try:

            n = int(
                input(
                    "행렬의 크기 n을 입력하세요: "
                )
            )

            if n <= 0:

                print(
                    "[오류] "
                    "n은 1 이상의 정수여야 합니다."
                )

                continue

            break

        except ValueError:

            print(
                "[오류] "
                "정수를 입력해주세요."
            )

    # -----------------------------------------------------
    # 행렬 입력
    # -----------------------------------------------------
    matrix = []

    print(
        f"\n{n} × {n} 행렬을 "
        f"행 단위로 입력하세요."
    )

    print(
        "(각 원소는 공백으로 구분합니다.)"
    )

    for i in range(n):

        while True:

            try:

                row = list(
                    map(
                        float,
                        input(
                            f"{i + 1}행: "
                        ).split()
                    )
                )

                if len(row) != n:

                    print(
                        f"[오류] 원소를 "
                        f"정확히 {n}개 "
                        f"입력해주세요."
                    )

                    continue

                matrix.append(row)
                break

            except ValueError:

                print(
                    "[오류] "
                    "숫자만 입력해주세요."
                )

    # -----------------------------------------------------
    # 입력 행렬 출력
    # -----------------------------------------------------
    print("\n[입력한 행렬]")

    print_matrix(matrix)

    # -----------------------------------------------------
    # 행렬식을 이용한 역행렬 계산
    # -----------------------------------------------------
    inverse_det = (
        inverse_by_determinant(
            matrix
        )
    )

    # -----------------------------------------------------
    # 가우스-조던을 이용한 역행렬 계산
    # -----------------------------------------------------
    inverse_gauss = (
        inverse_by_gauss_jordan(
            matrix
        )
    )

    # =====================================================
    # 최종 결과
    # =====================================================
    print(
        "\n========== "
        "최종 결과 "
        "=========="
    )

    # 행렬식 방법
    print(
        "\n[행렬식을 이용한 역행렬]"
    )

    if inverse_det is None:

        print(
            "역행렬이 존재하지 않습니다."
        )

    else:

        print_matrix(
            inverse_det
        )

    # 가우스-조던 방법
    print(
        "\n[가우스-조던 소거법을 "
        "이용한 역행렬]"
    )

    if inverse_gauss is None:

        print(
            "역행렬이 존재하지 않습니다."
        )

    else:

        print_matrix(
            inverse_gauss
        )

    # -----------------------------------------------------
    # 두 결과 비교
    # -----------------------------------------------------
    print(
        "\n[두 결과 비교]"
    )

    if (
        inverse_det is None
        and inverse_gauss is None
    ):

        print(
            "두 방법 모두 "
            "역행렬이 존재하지 않는다고 "
            "판정했습니다."
        )

    elif (
        inverse_det is None
        or inverse_gauss is None
    ):

        print(
            "두 방법의 결과가 "
            "서로 다릅니다."
        )

    elif are_matrices_equal(
        inverse_det,
        inverse_gauss
    ):

        print(
            "두 방법으로 계산한 "
            "역행렬이 동일합니다."
        )

    else:

        print(
            "두 방법으로 계산한 "
            "역행렬이 서로 다릅니다."
        )


# 프로그램 실행
main()