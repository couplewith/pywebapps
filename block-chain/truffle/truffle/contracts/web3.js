
Web3 = require('web3')
web3 = new Web3("http://localhost:8545")


bytecode=fs.readFileSync('SimpleStorage_sol_SimpleStorage.bin').toString()
abi=JSON.parse(fs.readFileSync('SimpleStorage_sol_SimpleStorage.abi').toString())

notorizedContract = new web3.eth.Contract(abi)


notorizedContract.deploy({ data: bytecode }).send({
  from: '0x397993Ea65516Aeb88e2db9773c35a18209ceC16',
  gas: 1000000, // Increase the gas amount if needed
  gasPrice: web3.utils.toWei('0.00003', 'ether'),
}).then((newContractInstance) => {
  notorizedContract.options.address = newContractInstance.options.address;
});

notorizedContract.deploy({data:bytecode}).send({
  from:'0x397993Ea65516Aeb88e2db9773c35a18209ceC16',
  gas:1000,
  gasPrice:web3.utils.toWei('0.00003','ether'),
}).then((newContractInstance) => {
   notorizedContract.option.address=newContractionInstalnce.options.address});
