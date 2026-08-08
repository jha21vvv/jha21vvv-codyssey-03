from simulator import MACSimulator

def main():
    # 시뮬레이터 객체를 만들고 실행합니다.
    app = MACSimulator() #맥시뮬레이터 기반으로 app라는걸 맥시뮬레이터를 만들어서
    app.run()#실행

if __name__ == "__main__":
    main()