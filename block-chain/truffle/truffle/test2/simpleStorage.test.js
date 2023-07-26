// 스마트 계약을 테스트하기 위해 필요한 객체들을 가져옵니다.
const SimpleStorage = artifacts.require("SimpleStorage");

// SimpleStorage 컨트랙트의 테스트 코드
contract("SimpleStorage", accounts => {
    // 계약이 정상적으로 배포되었는지 확인합니다.
    it("should deploy smart contract properly", async () => {
        const simpleStorage = await SimpleStorage.deployed();
        assert(simpleStorage.address !== "");
    });

    // 데이터를 저장하고 읽는 기능을 테스트합니다.
    it("should set and get data correctly", async () => {
        const simpleStorage = await SimpleStorage.deployed();

        // 데이터를 설정하고 저장합니다.
        const dataToSet = 42;
        await simpleStorage.setData(dataToSet);

        // 데이터를 읽어옵니다.
        const data = await simpleStorage.getData();

        // 데이터가 정확하게 저장되었는지 확인합니다.
        assert.equal(data, dataToSet, "Data was not set correctly.");
    });
});

