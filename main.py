import math

scale = 16

def twos_comp(val, bits):
    """compute the 2's complement of int value val"""
    if (val & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
        val = val - (1 << bits)        # compute negative value
    return val                         # return positive value as is

def registerToName(regNum):
	if regNum == "00000":
		return "x0"
	if regNum == "00001":
		return "ra"
	if regNum == "00010":
		return "sp"
	if regNum == "00011":
		return "gp"
	if regNum == "00100":
		return "tp"
	if regNum == "00101":
		return "t0"
	if regNum == "00110":
		return "t1"
	if regNum == "00111":
		return "t2"
	if regNum == "01000":
		return "s0"
	if regNum == "01001":
		return "s1"
	if regNum == "01010":
		return "a0"
	if regNum == "01011":
		return "a1"
	if regNum == "01100":
		return "a2"
	if regNum == "01101":
		return "a3"
	if regNum == "01110":
		return "a4"
	if regNum == "01111":
		return "a5"
	if regNum == "10000":
		return "a6"
	if regNum == "10001":
		return "a7"
	if regNum == "10010":
		return "s2"
	if regNum == "10011":
		return "s3"
	if regNum == "10100":
		return "s4"
	if regNum == "10101":
		return "s5"
	if regNum == "10110":
		return "s6"
	if regNum == "10111":
		return "s7"
	if regNum == "11000":
		return "s8"
	if regNum == "11001":
		return "s9"
	if regNum == "11010":
		return "s10"
	if regNum == "11011":
		return "s11"
	if regNum == "11100":
		return "t3"
	if regNum == "11101":
		return "t4"
	if regNum == "11110":
		return "t5"
	if regNum == "11111":
		return "t6"



def converter(binary):
	opcode = binary[-7:]
	#print(opcode)
	if opcode == "0110011":
		return R(binary)
	elif opcode == "0000011":
		return loadI(binary)
	elif opcode == "0010011":
		return ariI(binary)
	elif opcode == "0100011":
		return S(binary)
	elif opcode == "1100011":
			return B(binary)
	elif opcode == "0010111":
			return auipc(binary)
	elif opcode == "0110111":
			return lui(binary)
	elif opcode == "1101111":
			return jal(binary)
	elif opcode == "1100111":
			return jalr(binary)
	elif opcode == "1110011":
			return csrw(binary)
	elif opcode == "0100011":
			return csrwi(binary)

def R(binary):
	rd = binary[20:25]
	funct3 = binary[17:20]
	rs1 = binary[12:17]
	rs2 = binary[7:12]
	funct7 = binary[0:7]
	if funct7 == "0000000":
		if funct3 == "000":
			operation = "add"
		elif funct3 == "001":
			operation = "sll"
		elif funct3 == "010":
			operation = "slt"
		elif funct3 == "100":
			operation = "xor"
		elif funct3 == "101":
			operation = "srl"
		elif funct3 == "110":
			operation = "or"
		elif funct3 == "111":
			operation = "and"
	elif funct7 == "0000001":
		if funct3 == "000":
			operation = "mul"
		elif funct3 == "001":
			operation = "mulh"
		elif funct3 == "011":
			operation = "mulhu"
	elif funct7 == "010000":
		if funct3 == "000":
			operation = "sub"
		elif funct3 == "101":
			operation = "sra"

	return '{0} {1}, {2}, {3}'.format(operation, registerToName(rd), registerToName(rs1), registerToName(rs2))



def ariI(binary):
	rd = binary[20:25]
	funct3 = binary[17:20]
	rs1 = binary[12:17]
	imm = binary[0:12]
	print(binary)
	print(imm)
	print(rs1)
	print(rd)


	shiftrightimm = binary[7:12]
	funct7 = binary[0:7]

	if funct3 == "000":
			operation = "addi"
	elif funct3 == "001":
			operation = "slli"
	elif funct3 == "010":
			operation = "slti"
	elif funct3 == "100":
			operation = "xori"
	elif funct3 == "101":
		if funct7 == "0000000":
			operation = "srli"
		else:
			operation = "srai"
			return '{0} {1}, {2}, {3}'.format(operation, registerToName(rd), registerToName(rs1), int(shiftrightimm, 2))
	elif funct3 == "110":
			operation = "ori"
	elif funct3 == "111":
			operation = "andi"
	return '{0} {1}, {2}, {3}'.format(operation, registerToName(rd), registerToName(rs1), twos_comp(int(imm, 2), len(imm)))

def loadI(binary):
	rd = binary[20:25]
	funct3 = binary[17:20]
	rs1 = binary[12:17]
	imm = binary[0:12]

	if funct3 == "000":
			operation = "lb"
	elif funct3 == "001":
			operation = "lh"
	elif funct3 == "010":
			operation = "lw"

	return '{0} {1}, {3}({2})'.format(operation, registerToName(rd), registerToName(rs1), twos_comp(int(imm, 2), len(imm)))

def S(binary):
	immLow = binary[20:25]
	funct3 = binary[17:20]
	rs1 = binary[12:17]
	rs2 = binary[7:12]
	immHigh = binary[0:7]

	imm = immHigh + immLow

	if funct3 == "000":
			operation = "sb"
	elif funct3 == "001":
			operation = "sh"
	elif funct3 == "010":
			operation = "sw"


	return '{0} {1}, {3}({2})'.format(operation, registerToName(rs2), registerToName(rs1), twos_comp(int(imm, 2), len(imm)))

def B(binary):
	print("B") 
	immLow = binary[20:25]
	funct3 = binary[17:20]
	rs1 = binary[12:17]
	rs2 = binary[7:12]
	immHigh = binary[0:7]

	imm = immHigh[0] + immLow[-1] + immHigh[1:] + immLow[:-1] + "0"

	if funct3 == "000":
			operation = "beq"
	elif funct3 == "001":
			operation = "bne"
	elif funct3 == "100":
			operation = "blt"
	elif funct3 == "101":
			operation = "bge"
	elif funct3 == "110":
			operation = "bltu"
	elif funct3 == "111":
			operation = "bgeu"

	return '{0} {1}, {2}, {3}'.format(operation, registerToName(rs1), registerToName(rs2), twos_comp(int(imm, 2), len(imm)))

def auipc(binary):
	rd = binary[20:25]
	imm = binary[:20] + 12*"0"
	return 'auipc {0}, {1}'.format(rd, twos_comp(int(imm, 2), len(imm)))

def lui(binary):
	rd = binary[20:25]
	imm = binary[:20] + 12*"0"
	return 'lui {0}, {1}'.format(rd, twos_comp(int(imm, 2), len(imm)))

def jal(binary):
	rd = binary[20:25]
	immScrambled = binary[:20]
	imm = immScrambled[0] + immScrambled[12:20] + immScrambled[11] + immScrambled[1:11]
	return 'jal {0}, {1}'.format(rd, twos_comp(int(imm, 2), len(imm)))

def jalr(binary):
	rd = binary[20:25]
	rs1 = binary[12:17]
	imm = binary[0:12]

	return 'jalr {0}, {1}, {2}'.format(registerToName(rd), registerToName(rs1), twos_comp(int(imm, 2), len(imm)))


def csrw(binary):

	rd = binary[20:25]
	funct3 = binary[17:20]
	rs1 = binary[12:17]
	csr = binary[0:12]
	print(rs1)
	print(rd)
	if funct3 == "001":
		return 'csrw {0}, {1}, {2}'.format(registerToName(rd), csr, registerToName(rs1))
	else:
		return 'csrwi {0}, {1}, {2}'.format(registerToName(rd), csr, int(rs1, 2))

def main():
	num = "0x00000000"
	while num.lower() != "stop":
		num = input("\nEnter either hex or binary number, with 0x prefix for hex and 0b prefix for binary.\n")
		if num[:2] == "0x":
				num = bin(int(num[:29], scale))[2:]
				#print(num)
				num = num.zfill(32)
		else:
				num = num[2:]
		#print(num)
		print(converter(num))



if __name__ == "__main__":
	main()
