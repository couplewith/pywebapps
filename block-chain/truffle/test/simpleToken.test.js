const SimpleToken = artifacts.require("SimpleToken");

contract("SimpleToken", accounts => {
    it("should deploy smart contract properly", async () => {
        const simpleToken = await SimpleToken.deployed();
        assert(simpleToken.address !== "");
    });

    it("should getBalance and transfer correctly", async () => {
        const simpleToken = await SimpleToken.deployed();

        const ownerAccount = "0xcb609870f66bc11aeA64767AEA2135880d25b48A";
        const ownerAmt = await simpleToken.getBalance(ownerAccount);

        const sendAmt = 33;
        const recvAccount = "0xe28429D69B659D7Ad803bE291D7c2faCF829582F";
        await simpleToken.transfer(recvAccount, sendAmt);

        const ownerAmt2 = await simpleToken.getBalance(ownerAccount);
        const recvAmt = await simpleToken.getBalance(recvAccount);

        assert.equal(ownerAmt.toNumber(), ownerAmt2.toNumber(), "Owner balance was not set correctly.");
        assert.equal(recvAmt.toNumber(), sendAmt, "Receiver balance was not set correctly.");
    });
});

