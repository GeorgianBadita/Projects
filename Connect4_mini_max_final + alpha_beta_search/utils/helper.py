"""
    @author: Badita Marin-Georgian
    @email:  geo.badita@gmail.com
    @date:   12/17/2017 17:27
"""


def check_4_line(matrix):
    """
    Checks if there are 4 equal values on the same line
    :param matrix: matrix
    :return: True if there are 4 equal values on the same line,
     False otherwise
    """

    max_width = len(matrix[0])

    for line in range(len(matrix)):
        for col in range(len(matrix[0])):
            if matrix[line][col] != 0:
                num_eq = 1
                for verif in range(3):
                    if col + verif + 1 < max_width and matrix[line][col + verif] == matrix[line][col + verif + 1]:
                        num_eq += 1
                if num_eq == 4:
                    # print(matrix[line][col])
                    return True
    return False


def check_4_diag(matrix):
    """
    Checks if there are 4 equal values on the same diagonal
    :param matrix: matrix
    :return: True if there are 4 equal values on the same diagonal,
     False otherwise
    """
    max_height = len(matrix)
    max_width = len(matrix[0])

    for line in range(len(matrix)):
        for col in range(len(matrix[0])):
            if matrix[line][col] != 0:
                num_eq = 1
                for verif in range(3):
                    if col + verif + 1 < max_width and line + verif + 1 < max_height and matrix[line + verif][
                        col + verif] == matrix[line + verif + 1][col + verif + 1]:
                        num_eq += 1
                if num_eq == 4:
                    # print(matrix[line][col])
                    return True
                else:
                    num_eq = 1
                    for verif in range(3):
                        if col - verif >= 1 and line + verif + 1 < max_height and matrix[line + verif][col - verif] == \
                                matrix[line + verif + 1][col - verif - 1]:
                            num_eq += 1
                    if num_eq == 4:
                        # print(matrix[line][col])
                        return True
    return False


def check_4_col(matrix):
    """
    Checks if there are 4 equal values on the same column
    :param matrix: matrix
    :return: True if there are 4 equal values on the same column,
     False otherwise
    """
    max_height = len(matrix)

    for line in range(len(matrix)):
        for col in range(len(matrix[0])):
            if matrix[line][col] != 0:
                num_eq = 1
                for verif in range(3):
                    if line + verif + 1 < max_height and matrix[line + verif][col] == matrix[line + verif + 1][col]:
                        num_eq += 1
                if num_eq == 4:
                    # print(matrix[line][col])
                    return True
    return False
