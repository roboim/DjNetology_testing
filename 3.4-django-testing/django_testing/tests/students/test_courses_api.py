import pytest


class TestApi:
    main_path = "/api/v1/"
    test_path = "courses/"

    @pytest.mark.django_db
    def test_get_one_course(self, client, course_factory):
        """Проверка получения первого курса (retrieve-логика)"""
        # Arrange
        course_1 = course_factory(_quantity=1)
        # Act
        response = client.get(self.main_path + self.test_path + f'{course_1[0].id}/')
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert course_1[0].name == data['name']


    @pytest.mark.django_db
    def test_get_courses(self, client, course_factory):
        """Проверка получения списка курсов (list-логика)"""
        # Arrange
        course_1 = course_factory(_quantity=1)
        # Act
        response = client.get(self.main_path + self.test_path)
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert course_1[0].name == data[0]['name']

    @pytest.mark.django_db
    def test_course_id_filter(self, client, course_factory):
        """Проверка фильтрации списка курсов по id"""
        # Arrange
        courses = course_factory(_quantity=5)
        course_id = courses[2].pk
        # Act
        response = client.get(self.main_path + self.test_path + f'?id={course_id}')
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert courses[2].name == data[0]['name']

    @pytest.mark.django_db
    def test_course_name_filter(self, client, course_factory):
        """Проверка фильтрации списка курсов по name"""
        # Arrange
        courses = course_factory(_quantity=5)
        course_name = courses[2].name
        # Act
        response = client.get(self.main_path + self.test_path + f'?name={course_name}')
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert courses[2].name == data[0]['name']

    @pytest.mark.django_db
    def test_make_course(self, client):
        """Проверка создания одного курса"""
        # Arrange
        course_data = {
            'name': 'test_name'
        }
        # Act
        response = client.post(self.main_path + self.test_path, data=course_data)
        # Assert
        assert response.status_code == 201
        data = response.json()
        assert course_data['name'] == data['name']
        assert data['students'] == []

    @pytest.mark.django_db
    def test_adj_course(self, client, course_factory):
        """Проверка полной замены одного курса"""
        # Arrange
        course_data = {
            'id': 0,
            'name': 'test_name',
            'students': []
        }
        courses = course_factory(_quantity=5)
        course_data['id'] = courses[2].id
        # Act
        response = client.put(self.main_path + self.test_path + f'{course_data["id"]}/', data=course_data)
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert course_data['name'] == data['name']
        assert data['students'] == []

    @pytest.mark.django_db
    def test_delete_course(self, client, course_factory):
        """Проверка удаления одного курса"""
        # Arrange
        courses = course_factory(_quantity=5)
        target_course_number = courses[2].id
        # Act
        response1 = client.delete(self.main_path + self.test_path + f'{target_course_number}/')
        # Assert
        assert response1.status_code == 204
        # Act
        response2 = client.get(self.main_path + self.test_path)
        # Assert
        assert response2.status_code == 200
        data = response2.json()
        assert len(data) == 4
