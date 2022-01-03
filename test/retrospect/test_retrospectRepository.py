from assertpy import assert_that

from main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_회고_정상적으로_생성():
    # given
    """
    @:param: 사진, 루틴 아이디, 내용, 유저 아이디
    루틴 사전 생성
    :return:
    """
    # when
    """
    repository 불러서 해당 값을 넣는다. 
    """
    # then
    """
    조회를 통해 해당 값이 잘 들어가 있는 지 확인
    """


def test_회고_생성_실패_이미지_파라미터가_없을_때():
    # given
    """
    @:parameter: 사진(x), 루틴 아이디, 내용, 유저 아이디
    루틴 사전 생성
    :return:
    """
    # when
    """
    repository 불러서 해당 값을 넣는다.(이미지가 없음)
    """
    # then
    """
    에러 확인
    """

def test_회고_생성_실패_루틴_정보가_없을_때():
    # given
    """
    @:parameter: 사진, 내용, 루틴 아이디 x, 유저 아이디
    :return:
    """
    # when
    """
    생성 시도
    """
    # then
    """
    에러 확인
    """

def test_회고_수정할_때_이미지에_대해서():
    # given
    """
    @:parameter: 이미지, 회고 아이디, 유저 아이디
    :return:
    """
    # when
    """
    사전 오늘날짜 확인해서 수요일 이전인지 확인
    기존 이미지 삭제 및 새 이미지 아이디와 회고 아이디 연결
    성공 여부 전달
    """
    # then
    """
    성공 여부 전달
    """

def test_회고_수정할_때_글_내용_수정할_때():
    # given
    """
    @:parameter: 회고 아이디, 글 내용, 유저 아이디
    :return:
    """
    # when
    """
    오늘날짜 확인해서 수요일 이전인지 확인
    기존 콘텐츠 날리고 새 콘텐츠로 변경
    """
    # then
    """
    성공 여부 전달
    """

def test_회고_삭제할_때():
    # given
    """
    @:parameter: 회고 아이디, 유저 아이디
    :return:
    """
    # when
    """
    삭제 진행
    삭제 진행할 때 회고 내용만 삭제되고 이에 대한 수행 여부는 존재해야 한다.
    """
    # then
    """
    성공 여부 전달
    """
