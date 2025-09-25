#
# Copyright (c) 2024, Massachusetts Institute of Technology All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# Redistributions of source code must retain the above copyright notice, this
# list of conditions and the following disclaimer.
#
# Redistributions in binary form must reproduce the above copyright notice, this
# list of conditions and the following disclaimer in the documentation and/or
# other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

from .descriptors import Function

def d(conn=None):
    return Function(0, conn=conn)

def dA0(conn=None):
    return Function(1, conn=conn)

def dALPHA(conn=None):
    return Function(2, conn=conn)

def dAMU(conn=None):
    return Function(3, conn=conn)

def dC(conn=None):
    return Function(4, conn=conn)

def dCAL(conn=None):
    return Function(5, conn=conn)

def dDEGREE(conn=None):
    return Function(6, conn=conn)

def dEV(conn=None):
    return Function(7, conn=conn)

def dFALSE(conn=None):
    return Function(8, conn=conn)

def dFARADAY(conn=None):
    return Function(9, conn=conn)

def dG(conn=None):
    return Function(10, conn=conn)

def dGAS(conn=None):
    return Function(11, conn=conn)

def dH(conn=None):
    return Function(12, conn=conn)

def dHBAR(conn=None):
    return Function(13, conn=conn)

def dI(conn=None):
    return Function(14, conn=conn)

def dK(conn=None):
    return Function(15, conn=conn)

def dME(conn=None):
    return Function(16, conn=conn)

def dMISSING(conn=None):
    return Function(17, conn=conn)

def dMP(conn=None):
    return Function(18, conn=conn)

def dN0(conn=None):
    return Function(19, conn=conn)

def dNA(conn=None):
    return Function(20, conn=conn)

def dP0(conn=None):
    return Function(21, conn=conn)

def dPI(conn=None):
    return Function(22, conn=conn)

def dQE(conn=None):
    return Function(23, conn=conn)

def dRE(conn=None):
    return Function(24, conn=conn)

def dROPRAND(conn=None):
    return Function(25, conn=conn)

def dRYDBERG(conn=None):
    return Function(26, conn=conn)

def dT0(conn=None):
    return Function(27, conn=conn)

def dTORR(conn=None):
    return Function(28, conn=conn)

def dTRUE(conn=None):
    return Function(29, conn=conn)

def dVALUE(conn=None):
    return Function(30, conn=conn)

def ABORT(*args, conn=None):
    return Function(31, *args, conn=conn)

def ABS(*args, conn=None):
    return Function(32, *args, conn=conn)

def ABS1(*args, conn=None):
    return Function(33, *args, conn=conn)

def ABSSQ(*args, conn=None):
    return Function(34, *args, conn=conn)

def ACHAR(*args, conn=None):
    return Function(35, *args, conn=conn)

def ACOS(*args, conn=None):
    return Function(36, *args, conn=conn)

def ACOSD(*args, conn=None):
    return Function(37, *args, conn=conn)

def ADD(*args, conn=None):
    return Function(38, *args, conn=conn)

def ADJUSTL(*args, conn=None):
    return Function(39, *args, conn=conn)

def ADJUSTR(*args, conn=None):
    return Function(40, *args, conn=conn)

def AIMAG(*args, conn=None):
    return Function(41, *args, conn=conn)

def AINT(*args, conn=None):
    return Function(42, *args, conn=conn)

def ALL(*args, conn=None):
    return Function(43, *args, conn=conn)

def ALLOCATED(*args, conn=None):
    return Function(44, *args, conn=conn)

def AND(*args, conn=None):
    return Function(45, *args, conn=conn)

def AND_NOT(*args, conn=None):
    return Function(46, *args, conn=conn)

def ANINT(*args, conn=None):
    return Function(47, *args, conn=conn)

def ANY(*args, conn=None):
    return Function(48, *args, conn=conn)

def ARG(*args, conn=None):
    return Function(49, *args, conn=conn)

def ARGD(*args, conn=None):
    return Function(50, *args, conn=conn)

def ARG_OF(*args, conn=None):
    return Function(51, *args, conn=conn)

def ARRAY(*args, conn=None):
    return Function(52, *args, conn=conn)

def ASIN(*args, conn=None):
    return Function(53, *args, conn=conn)

def ASIND(*args, conn=None):
    return Function(54, *args, conn=conn)

def AS_IS(*args, conn=None):
    return Function(55, *args, conn=conn)

def ATAN(*args, conn=None):
    return Function(56, *args, conn=conn)

def ATAN2(*args, conn=None):
    return Function(57, *args, conn=conn)

def ATAN2D(*args, conn=None):
    return Function(58, *args, conn=conn)

def ATAND(*args, conn=None):
    return Function(59, *args, conn=conn)

def ATANH(*args, conn=None):
    return Function(60, *args, conn=conn)

def AXIS_OF(*args, conn=None):
    return Function(61, *args, conn=conn)

def BACKSPACE(*args, conn=None):
    return Function(62, *args, conn=conn)

def IBCLR(*args, conn=None):
    return Function(63, *args, conn=conn)

def BEGIN_OF(*args, conn=None):
    return Function(64, *args, conn=conn)

def IBITS(*args, conn=None):
    return Function(65, *args, conn=conn)

def BREAK(conn=None):
    return Function(66, conn=conn)

def BSEARCH(*args, conn=None):
    return Function(67, *args, conn=conn)

def IBSET(*args, conn=None):
    return Function(68, *args, conn=conn)

def BTEST(*args, conn=None):
    return Function(69, *args, conn=conn)

def BUILD_ACTION(*args, conn=None):
    return Function(70, *args, conn=conn)

def BUILD_CONDITION(*args, conn=None):
    return Function(71, *args, conn=conn)

def BUILD_CONGLOM(*args, conn=None):
    return Function(72, *args, conn=conn)

def BUILD_DEPENDENCY(*args, conn=None):
    return Function(73, *args, conn=conn)

def BUILD_DIM(*args, conn=None):
    return Function(74, *args, conn=conn)

def BUILD_DISPATCH(*args, conn=None):
    return Function(75, *args, conn=conn)

def BUILD_EVENT(*args, conn=None):
    return Function(76, *args, conn=conn)

def BUILD_FUNCTION(*args, conn=None):
    return Function(77, *args, conn=conn)

def BUILD_METHOD(*args, conn=None):
    return Function(78, *args, conn=conn)

def BUILD_PARAM(*args, conn=None):
    return Function(79, *args, conn=conn)

def BUILD_PATH(*args, conn=None):
    return Function(80, *args, conn=conn)

def BUILD_PROCEDURE(*args, conn=None):
    return Function(81, *args, conn=conn)

def BUILD_PROGRAM(*args, conn=None):
    return Function(82, *args, conn=conn)

def BUILD_RANGE(*args, conn=None):
    return Function(83, *args, conn=conn)

def BUILD_ROUTINE(*args, conn=None):
    return Function(84, *args, conn=conn)

def BUILD_SIGNAL(*args, conn=None):
    return Function(85, *args, conn=conn)

def BUILD_SLOPE(*args, conn=None):
    return Function(86, *args, conn=conn)

def BUILD_WINDOW(*args, conn=None):
    return Function(87, *args, conn=conn)

def BUILD_WITH_UNITS(*args, conn=None):
    return Function(88, *args, conn=conn)

def BUILTIN_OPCODE(*args, conn=None):
    return Function(89, *args, conn=conn)

def BYTE(*args, conn=None):
    return Function(90, *args, conn=conn)

def BYTE_UNSIGNED(*args, conn=None):
    return Function(91, *args, conn=conn)

def CASE(*args, conn=None):
    return Function(92, *args, conn=conn)

def CEILING(*args, conn=None):
    return Function(93, *args, conn=conn)

def CHAR(*args, conn=None):
    return Function(94, *args, conn=conn)

def CLASS(*args, conn=None):
    return Function(95, *args, conn=conn)

def FCLOSE(*args, conn=None):
    return Function(96, *args, conn=conn)

def CMPLX(*args, conn=None):
    return Function(97, *args, conn=conn)

def COMMA(*args, conn=None):
    return Function(98, *args, conn=conn)

def COMPILE(*args, conn=None):
    return Function(99, *args, conn=conn)

def COMPLETION_OF(*args, conn=None):
    return Function(100, *args, conn=conn)

def CONCAT(*args, conn=None):
    return Function(101, *args, conn=conn)

def CONDITIONAL(*args, conn=None):
    return Function(102, *args, conn=conn)

def CONJG(*args, conn=None):
    return Function(103, *args, conn=conn)

def CONTINUE(conn=None):
    return Function(104, conn=conn)

def CONVOLVE(*args, conn=None):
    return Function(105, *args, conn=conn)

def COS(*args, conn=None):
    return Function(106, *args, conn=conn)

def COSD(*args, conn=None):
    return Function(107, *args, conn=conn)

def COSH(*args, conn=None):
    return Function(108, *args, conn=conn)

def COUNT(*args, conn=None):
    return Function(109, *args, conn=conn)

def CSHIFT(*args, conn=None):
    return Function(110, *args, conn=conn)

def CVT(*args, conn=None):
    return Function(111, *args, conn=conn)

def DATA(*args, conn=None):
    return Function(112, *args, conn=conn)

def DATE_AND_TIME(*args, conn=None):
    return Function(113, *args, conn=conn)

def DATE_TIME(*args, conn=None):
    return Function(114, *args, conn=conn)

def DBLE(*args, conn=None):
    return Function(115, *args, conn=conn)

def DEALLOCATE(*args, conn=None):
    return Function(116, *args, conn=conn)

def DEBUG(*args, conn=None):
    return Function(117, *args, conn=conn)

def DECODE(*args, conn=None):
    return Function(118, *args, conn=conn)

def DECOMPILE(*args, conn=None):
    return Function(119, *args, conn=conn)

def DECOMPRESS(*args, conn=None):
    return Function(120, *args, conn=conn)

def DEFAULT(*args, conn=None):
    return Function(121, *args, conn=conn)

def DERIVATIVE(*args, conn=None):
    return Function(122, *args, conn=conn)

def DESCR(*args, conn=None):
    return Function(123, *args, conn=conn)

def DIAGONAL(*args, conn=None):
    return Function(124, *args, conn=conn)

def DIGITS(*args, conn=None):
    return Function(125, *args, conn=conn)

def DIM(*args, conn=None):
    return Function(126, *args, conn=conn)

def DIM_OF(*args, conn=None):
    return Function(127, *args, conn=conn)

def DISPATCH_OF(*args, conn=None):
    return Function(128, *args, conn=conn)

def DIVIDE(*args, conn=None):
    return Function(129, *args, conn=conn)

def LBOUND(*args, conn=None):
    return Function(130, *args, conn=conn)

def DO(*args, conn=None):
    return Function(131, *args, conn=conn)

def DOT_PRODUCT(*args, conn=None):
    return Function(132, *args, conn=conn)

def DPROD(*args, conn=None):
    return Function(133, *args, conn=conn)

def DSCPTR(*args, conn=None):
    return Function(134, *args, conn=conn)

def SHAPE(*args, conn=None):
    return Function(135, *args, conn=conn)

def SIZE(*args, conn=None):
    return Function(136, *args, conn=conn)

def KIND(*args, conn=None):
    return Function(137, *args, conn=conn)

def UBOUND(*args, conn=None):
    return Function(138, *args, conn=conn)

def D_COMPLEX(*args, conn=None):
    return Function(139, *args, conn=conn)

def D_FLOAT(*args, conn=None):
    return Function(140, *args, conn=conn)

def RANGE(*args, conn=None):
    return Function(141, *args, conn=conn)

def PRECISION(*args, conn=None):
    return Function(142, *args, conn=conn)

def ELBOUND(*args, conn=None):
    return Function(143, *args, conn=conn)

def ELSE(conn=None):
    return Function(144, conn=conn)

def ELSEWHERE(conn=None):
    return Function(145, conn=conn)

def ENCODE(*args, conn=None):
    return Function(146, *args, conn=conn)

def ENDFILE(*args, conn=None):
    return Function(147, *args, conn=conn)

def END_OF(*args, conn=None):
    return Function(148, *args, conn=conn)

def EOSHIFT(*args, conn=None):
    return Function(149, *args, conn=conn)

def EPSILON(*args, conn=None):
    return Function(150, *args, conn=conn)

def EQ(*args, conn=None):
    return Function(151, *args, conn=conn)

def EQUALS(*args, conn=None):
    return Function(152, *args, conn=conn)

def EQUALS_FIRST(*args, conn=None):
    return Function(153, *args, conn=conn)

def EQV(*args, conn=None):
    return Function(154, *args, conn=conn)

def ESHAPE(*args, conn=None):
    return Function(155, *args, conn=conn)

def ESIZE(*args, conn=None):
    return Function(156, *args, conn=conn)

def EUBOUND(*args, conn=None):
    return Function(157, *args, conn=conn)

def EVALUATE(*args, conn=None):
    return Function(158, *args, conn=conn)

def EXECUTE(*args, conn=None):
    return Function(159, *args, conn=conn)

def EXP(*args, conn=None):
    return Function(160, *args, conn=conn)

def EXPONENT(*args, conn=None):
    return Function(161, *args, conn=conn)

def EXT_FUNCTION(*args, conn=None):
    return Function(162, *args, conn=conn)

def FFT(*args, conn=None):
    return Function(163, *args, conn=conn)

def FIRSTLOC(*args, conn=None):
    return Function(164, *args, conn=conn)

def FIT(*args, conn=None):
    return Function(165, *args, conn=conn)

def FIX_ROPRAND(*args, conn=None):
    return Function(166, *args, conn=conn)

def FLOAT(*args, conn=None):
    return Function(167, *args, conn=conn)

def FLOOR(*args, conn=None):
    return Function(168, *args, conn=conn)

def FOR(*args, conn=None):
    return Function(169, *args, conn=conn)

def FRACTION(*args, conn=None):
    return Function(170, *args, conn=conn)

def FUN(*args, conn=None):
    return Function(171, *args, conn=conn)

def F_COMPLEX(*args, conn=None):
    return Function(172, *args, conn=conn)

def F_FLOAT(*args, conn=None):
    return Function(173, *args, conn=conn)

def GE(*args, conn=None):
    return Function(174, *args, conn=conn)

def GETNCI(*args, conn=None):
    return Function(175, *args, conn=conn)

def GOTO(*args, conn=None):
    return Function(176, *args, conn=conn)

def GT(*args, conn=None):
    return Function(177, *args, conn=conn)

def G_COMPLEX(*args, conn=None):
    return Function(178, *args, conn=conn)

def G_FLOAT(*args, conn=None):
    return Function(179, *args, conn=conn)

def HELP_OF(*args, conn=None):
    return Function(180, *args, conn=conn)

def HUGE(*args, conn=None):
    return Function(181, *args, conn=conn)

def H_COMPLEX(*args, conn=None):
    return Function(182, *args, conn=conn)

def H_FLOAT(*args, conn=None):
    return Function(183, *args, conn=conn)

def IACHAR(*args, conn=None):
    return Function(184, *args, conn=conn)

def IAND(*args, conn=None):
    return Function(185, *args, conn=conn)

def IAND_NOT(*args, conn=None):
    return Function(186, *args, conn=conn)

def ICHAR(*args, conn=None):
    return Function(187, *args, conn=conn)

def IDENT_OF(*args, conn=None):
    return Function(188, *args, conn=conn)

def IF(*args, conn=None):
    return Function(189, *args, conn=conn)

def IF_ERROR(*args, conn=None):
    return Function(190, *args, conn=conn)

def IMAGE_OF(*args, conn=None):
    return Function(191, *args, conn=conn)

def IN(*args, conn=None):
    return Function(192, *args, conn=conn)

def INAND(*args, conn=None):
    return Function(193, *args, conn=conn)

def INAND_NOT(*args, conn=None):
    return Function(194, *args, conn=conn)

def INDEX(*args, conn=None):
    return Function(195, *args, conn=conn)

def INOR(*args, conn=None):
    return Function(196, *args, conn=conn)

def INOR_NOT(*args, conn=None):
    return Function(197, *args, conn=conn)

def INOT(*args, conn=None):
    return Function(198, *args, conn=conn)

def INOUT(*args, conn=None):
    return Function(199, *args, conn=conn)

def INQUIRE(*args, conn=None):
    return Function(200, *args, conn=conn)

def INT(*args, conn=None):
    return Function(201, *args, conn=conn)

def INTEGRAL(*args, conn=None):
    return Function(202, *args, conn=conn)

def INTERPOL(*args, conn=None):
    return Function(203, *args, conn=conn)

def INTERSECT(*args, conn=None):
    return Function(204, *args, conn=conn)

def INT_UNSIGNED(*args, conn=None):
    return Function(205, *args, conn=conn)

def INVERSE(*args, conn=None):
    return Function(206, *args, conn=conn)

def IOR(*args, conn=None):
    return Function(207, *args, conn=conn)

def IOR_NOT(*args, conn=None):
    return Function(208, *args, conn=conn)

def IS_IN(*args, conn=None):
    return Function(209, *args, conn=conn)

def IEOR(*args, conn=None):
    return Function(210, *args, conn=conn)

def IEOR_NOT(*args, conn=None):
    return Function(211, *args, conn=conn)

def LABEL(*args, conn=None):
    return Function(212, *args, conn=conn)

def LAMINATE(*args, conn=None):
    return Function(213, *args, conn=conn)

def LANGUAGE_OF(*args, conn=None):
    return Function(214, *args, conn=conn)

def LASTLOC(*args, conn=None):
    return Function(215, *args, conn=conn)

def LE(*args, conn=None):
    return Function(216, *args, conn=conn)

def LEN(*args, conn=None):
    return Function(217, *args, conn=conn)

def LEN_TRIM(*args, conn=None):
    return Function(218, *args, conn=conn)

def LGE(*args, conn=None):
    return Function(219, *args, conn=conn)

def LGT(*args, conn=None):
    return Function(220, *args, conn=conn)

def LLE(*args, conn=None):
    return Function(221, *args, conn=conn)

def LLT(*args, conn=None):
    return Function(222, *args, conn=conn)

def LOG(*args, conn=None):
    return Function(223, *args, conn=conn)

def LOG10(*args, conn=None):
    return Function(224, *args, conn=conn)

def LOG2(*args, conn=None):
    return Function(225, *args, conn=conn)

def LOGICAL(*args, conn=None):
    return Function(226, *args, conn=conn)

def LONG(*args, conn=None):
    return Function(227, *args, conn=conn)

def LONG_UNSIGNED(*args, conn=None):
    return Function(228, *args, conn=conn)

def LT(*args, conn=None):
    return Function(229, *args, conn=conn)

def MATMUL(*args, conn=None):
    return Function(230, *args, conn=conn)

def MAT_ROT(*args, conn=None):
    return Function(231, *args, conn=conn)

def MAT_ROT_INT(*args, conn=None):
    return Function(232, *args, conn=conn)

def MAX(*args, conn=None):
    return Function(233, *args, conn=conn)

def MAXEXPONENT(*args, conn=None):
    return Function(234, *args, conn=conn)

def MAXLOC(*args, conn=None):
    return Function(235, *args, conn=conn)

def MAXVAL(*args, conn=None):
    return Function(236, *args, conn=conn)

def MEAN(*args, conn=None):
    return Function(237, *args, conn=conn)

def MEDIAN(*args, conn=None):
    return Function(238, *args, conn=conn)

def MERGE(*args, conn=None):
    return Function(239, *args, conn=conn)

def METHOD_OF(*args, conn=None):
    return Function(240, *args, conn=conn)

def MIN(*args, conn=None):
    return Function(241, *args, conn=conn)

def MINEXPONENT(*args, conn=None):
    return Function(242, *args, conn=conn)

def MINLOC(*args, conn=None):
    return Function(243, *args, conn=conn)

def MINVAL(*args, conn=None):
    return Function(244, *args, conn=conn)

def MOD(*args, conn=None):
    return Function(245, *args, conn=conn)

def MODEL_OF(*args, conn=None):
    return Function(246, *args, conn=conn)

def MULTIPLY(*args, conn=None):
    return Function(247, *args, conn=conn)

def NAME_OF(*args, conn=None):
    return Function(248, *args, conn=conn)

def NAND(*args, conn=None):
    return Function(249, *args, conn=conn)

def NAND_NOT(*args, conn=None):
    return Function(250, *args, conn=conn)

def NDESC(*args, conn=None):
    return Function(251, *args, conn=conn)

def NE(*args, conn=None):
    return Function(252, *args, conn=conn)

def NEAREST(*args, conn=None):
    return Function(253, *args, conn=conn)

def NEQV(*args, conn=None):
    return Function(254, *args, conn=conn)

def NINT(*args, conn=None):
    return Function(255, *args, conn=conn)

def NOR(*args, conn=None):
    return Function(256, *args, conn=conn)

def NOR_NOT(*args, conn=None):
    return Function(257, *args, conn=conn)

def NOT(*args, conn=None):
    return Function(258, *args, conn=conn)

def OBJECT_OF(*args, conn=None):
    return Function(259, *args, conn=conn)

def OCTAWORD(*args, conn=None):
    return Function(260, *args, conn=conn)

def OCTAWORD_UNSIGNED(*args, conn=None):
    return Function(261, *args, conn=conn)

def ON_ERROR(*args, conn=None):
    return Function(262, *args, conn=conn)

def OPCODE_BUILTIN(*args, conn=None):
    return Function(263, *args, conn=conn)

def OPCODE_STRING(*args, conn=None):
    return Function(264, *args, conn=conn)

def FOPEN(*args, conn=None):
    return Function(265, *args, conn=conn)

def OPTIONAL(*args, conn=None):
    return Function(266, *args, conn=conn)

def OR(*args, conn=None):
    return Function(267, *args, conn=conn)

def OR_NOT(*args, conn=None):
    return Function(268, *args, conn=conn)

def OUT(*args, conn=None):
    return Function(269, *args, conn=conn)

def PACK(*args, conn=None):
    return Function(270, *args, conn=conn)

def PHASE_OF(*args, conn=None):
    return Function(271, *args, conn=conn)

def POST_DEC(*args, conn=None):
    return Function(272, *args, conn=conn)

def POST_INC(*args, conn=None):
    return Function(273, *args, conn=conn)

def POWER(*args, conn=None):
    return Function(274, *args, conn=conn)

def PRESENT(*args, conn=None):
    return Function(275, *args, conn=conn)

def PRE_DEC(*args, conn=None):
    return Function(276, *args, conn=conn)

def PRE_INC(*args, conn=None):
    return Function(277, *args, conn=conn)

def PRIVATE(*args, conn=None):
    return Function(278, *args, conn=conn)

def PROCEDURE_OF(*args, conn=None):
    return Function(279, *args, conn=conn)

def PRODUCT(*args, conn=None):
    return Function(280, *args, conn=conn)

def PROGRAM_OF(*args, conn=None):
    return Function(281, *args, conn=conn)

def PROJECT(*args, conn=None):
    return Function(282, *args, conn=conn)

def PROMOTE(*args, conn=None):
    return Function(283, *args, conn=conn)

def PUBLIC(*args, conn=None):
    return Function(284, *args, conn=conn)

def QUADWORD(*args, conn=None):
    return Function(285, *args, conn=conn)

def QUADWORD_UNSIGNED(*args, conn=None):
    return Function(286, *args, conn=conn)

def QUALIFIERS_OF(*args, conn=None):
    return Function(287, *args, conn=conn)

def RADIX(*args, conn=None):
    return Function(288, *args, conn=conn)

def RAMP(*args, conn=None):
    return Function(289, *args, conn=conn)

def RANDOM(*args, conn=None):
    return Function(290, *args, conn=conn)

def RANDOM_SEED(*args, conn=None):
    return Function(291, *args, conn=conn)

def DTYPE_RANGE(*args, conn=None):
    return Function(292, *args, conn=conn)

def RANK(*args, conn=None):
    return Function(293, *args, conn=conn)

def RAW_OF(*args, conn=None):
    return Function(294, *args, conn=conn)

def READ(*args, conn=None):
    return Function(295, *args, conn=conn)

def REAL(*args, conn=None):
    return Function(296, *args, conn=conn)

def REBIN(*args, conn=None):
    return Function(297, *args, conn=conn)

def REF(*args, conn=None):
    return Function(298, *args, conn=conn)

def REPEAT(*args, conn=None):
    return Function(299, *args, conn=conn)

def REPLICATE(*args, conn=None):
    return Function(300, *args, conn=conn)

def RESHAPE(*args, conn=None):
    return Function(301, *args, conn=conn)

def RETURN(*args, conn=None):
    return Function(302, *args, conn=conn)

def REWIND(*args, conn=None):
    return Function(303, *args, conn=conn)

def RMS(*args, conn=None):
    return Function(304, *args, conn=conn)

def ROUTINE_OF(*args, conn=None):
    return Function(305, *args, conn=conn)

def RRSPACING(*args, conn=None):
    return Function(306, *args, conn=conn)

def SCALE(*args, conn=None):
    return Function(307, *args, conn=conn)

def SCAN(*args, conn=None):
    return Function(308, *args, conn=conn)

def FSEEK(*args, conn=None):
    return Function(309, *args, conn=conn)

def SET_EXPONENT(*args, conn=None):
    return Function(310, *args, conn=conn)

def SET_RANGE(*args, conn=None):
    return Function(311, *args, conn=conn)

def ISHFT(*args, conn=None):
    return Function(312, *args, conn=conn)

def ISHFTC(*args, conn=None):
    return Function(313, *args, conn=conn)

def SHIFT_LEFT(*args, conn=None):
    return Function(314, *args, conn=conn)

def SHIFT_RIGHT(*args, conn=None):
    return Function(315, *args, conn=conn)

def SIGN(*args, conn=None):
    return Function(316, *args, conn=conn)

def SIGNED(*args, conn=None):
    return Function(317, *args, conn=conn)

def SIN(*args, conn=None):
    return Function(318, *args, conn=conn)

def SIND(*args, conn=None):
    return Function(319, *args, conn=conn)

def SINH(*args, conn=None):
    return Function(320, *args, conn=conn)

def SIZEOF(*args, conn=None):
    return Function(321, *args, conn=conn)

def SLOPE_OF(*args, conn=None):
    return Function(322, *args, conn=conn)

def SMOOTH(*args, conn=None):
    return Function(323, *args, conn=conn)

def SOLVE(*args, conn=None):
    return Function(324, *args, conn=conn)

def SORTVAL(*args, conn=None):
    return Function(325, *args, conn=conn)

def SPACING(*args, conn=None):
    return Function(326, *args, conn=conn)

def SPAWN(*args, conn=None):
    return Function(327, *args, conn=conn)

def SPREAD(*args, conn=None):
    return Function(328, *args, conn=conn)

def SQRT(*args, conn=None):
    return Function(329, *args, conn=conn)

def SQUARE(*args, conn=None):
    return Function(330, *args, conn=conn)

def STATEMENT(*args, conn=None):
    return Function(331, *args, conn=conn)

def STD_DEV(*args, conn=None):
    return Function(332, *args, conn=conn)

def STRING(*args, conn=None):
    return Function(333, *args, conn=conn)

def STRING_OPCODE(*args, conn=None):
    return Function(334, *args, conn=conn)

def SUBSCRIPT(*args, conn=None):
    return Function(335, *args, conn=conn)

def SUBTRACT(*args, conn=None):
    return Function(336, *args, conn=conn)

def SUM(*args, conn=None):
    return Function(337, *args, conn=conn)

def SWITCH(*args, conn=None):
    return Function(338, *args, conn=conn)

def SYSTEM_CLOCK(*args, conn=None):
    return Function(339, *args, conn=conn)

def TAN(*args, conn=None):
    return Function(340, *args, conn=conn)

def TAND(*args, conn=None):
    return Function(341, *args, conn=conn)

def TANH(*args, conn=None):
    return Function(342, *args, conn=conn)

def TASK_OF(*args, conn=None):
    return Function(343, *args, conn=conn)

def TEXT(*args, conn=None):
    return Function(344, *args, conn=conn)

def TIME_OUT_OF(*args, conn=None):
    return Function(345, *args, conn=conn)

def TINY(*args, conn=None):
    return Function(346, *args, conn=conn)

def TRANSFER(*args, conn=None):
    return Function(347, *args, conn=conn)

def TRANSPOSE_(*args, conn=None):
    return Function(348, *args, conn=conn)

def TRIM(*args, conn=None):
    return Function(349, *args, conn=conn)

def UNARY_MINUS(*args, conn=None):
    return Function(350, *args, conn=conn)

def UNARY_PLUS(*args, conn=None):
    return Function(351, *args, conn=conn)

def UNION(*args, conn=None):
    return Function(352, *args, conn=conn)

def UNITS(*args, conn=None):
    return Function(353, *args, conn=conn)

def UNITS_OF(*args, conn=None):
    return Function(354, *args, conn=conn)

def UNPACK(*args, conn=None):
    return Function(355, *args, conn=conn)

def UNSIGNED(*args, conn=None):
    return Function(356, *args, conn=conn)

def VAL(*args, conn=None):
    return Function(357, *args, conn=conn)

def VALIDATION_OF(*args, conn=None):
    return Function(358, *args, conn=conn)

def VALUE_OF(*args, conn=None):
    return Function(359, *args, conn=conn)

def VAR(*args, conn=None):
    return Function(360, *args, conn=conn)

def VECTOR(*args, conn=None):
    return Function(361, *args, conn=conn)

def VERIFY(*args, conn=None):
    return Function(362, *args, conn=conn)

def WAIT(*args, conn=None):
    return Function(363, *args, conn=conn)

def WHEN_OF(*args, conn=None):
    return Function(364, *args, conn=conn)

def WHERE(*args, conn=None):
    return Function(365, *args, conn=conn)

def WHILE(*args, conn=None):
    return Function(366, *args, conn=conn)

def WINDOW_OF(*args, conn=None):
    return Function(367, *args, conn=conn)

def WORD(*args, conn=None):
    return Function(368, *args, conn=conn)

def WORD_UNSIGNED(*args, conn=None):
    return Function(369, *args, conn=conn)

def WRITE(*args, conn=None):
    return Function(370, *args, conn=conn)

def ZERO(*args, conn=None):
    return Function(371, *args, conn=conn)

def d2PI(conn=None):
    return Function(372, conn=conn)

def dNARG(conn=None):
    return Function(373, conn=conn)

def ELEMENT(*args, conn=None):
    return Function(374, *args, conn=conn)

def RC_DROOP(*args, conn=None):
    return Function(375, *args, conn=conn)

def RESET_PRIVATE(conn=None):
    return Function(376, conn=conn)

def RESET_PUBLIC(conn=None):
    return Function(377, conn=conn)

def SHOW_PRIVATE(*args, conn=None):
    return Function(378, *args, conn=conn)

def SHOW_PUBLIC(*args, conn=None):
    return Function(379, *args, conn=conn)

def SHOW_VM(*args, conn=None):
    return Function(380, *args, conn=conn)

def TRANSLATE(*args, conn=None):
    return Function(381, *args, conn=conn)

def TRANSPOSE_MUL(*args, conn=None):
    return Function(382, *args, conn=conn)

def UPCASE(*args, conn=None):
    return Function(383, *args, conn=conn)

def USING(*args, conn=None):
    return Function(384, *args, conn=conn)

def VALIDATION(*args, conn=None):
    return Function(385, *args, conn=conn)

def dDEFAULT(conn=None):
    return Function(386, conn=conn)

def dEXPT(conn=None):
    return Function(387, conn=conn)

def dSHOT(conn=None):
    return Function(388, conn=conn)

def GETDBI(*args, conn=None):
    return Function(389, *args, conn=conn)

def CULL(*args, conn=None):
    return Function(390, *args, conn=conn)

def EXTEND(*args, conn=None):
    return Function(391, *args, conn=conn)

def I_TO_X(*args, conn=None):
    return Function(392, *args, conn=conn)

def X_TO_I(*args, conn=None):
    return Function(393, *args, conn=conn)

def MAP(*args, conn=None):
    return Function(394, *args, conn=conn)

def COMPILE_DEPENDENCY(*args, conn=None):
    return Function(395, *args, conn=conn)

def DECOMPILE_DEPENDENCY(*args, conn=None):
    return Function(396, *args, conn=conn)

def BUILD_CALL(*args, conn=None):
    return Function(397, *args, conn=conn)

def ERRORLOGS_OF(*args, conn=None):
    return Function(398, *args, conn=conn)

def PERFORMANCE_OF(*args, conn=None):
    return Function(399, *args, conn=conn)

def XD(*args, conn=None):
    return Function(400, *args, conn=conn)

def CONDITION_OF(*args, conn=None):
    return Function(401, *args, conn=conn)

def SORT(*args, conn=None):
    return Function(402, *args, conn=conn)

def dTHIS(conn=None):
    return Function(403, conn=conn)

def DATA_WITH_UNITS(*args, conn=None):
    return Function(404, *args, conn=conn)

def dATM(conn=None):
    return Function(405, conn=conn)

def dEPSILON0(conn=None):
    return Function(406, conn=conn)

def dGN(conn=None):
    return Function(407, conn=conn)

def dMU0(conn=None):
    return Function(408, conn=conn)

def EXTRACT(*args, conn=None):
    return Function(409, *args, conn=conn)

def FINITE(*args, conn=None):
    return Function(410, *args, conn=conn)

def BIT_SIZE(*args, conn=None):
    return Function(411, *args, conn=conn)

def MODULO(*args, conn=None):
    return Function(412, *args, conn=conn)

def SELECTED_INT_KIND(*args, conn=None):
    return Function(413, *args, conn=conn)

def SELECTED_REAL_KIND(*args, conn=None):
    return Function(414, *args, conn=conn)

def DSQL(*args, conn=None):
    return Function(415, *args, conn=conn)

def ISQL(*args, conn=None):
    return Function(416, *args, conn=conn)

def FTELL(*args, conn=None):
    return Function(417, *args, conn=conn)

def MAKE_ACTION(*args, conn=None):
    return Function(418, *args, conn=conn)

def MAKE_CONDITION(*args, conn=None):
    return Function(419, *args, conn=conn)

def MAKE_CONGLOM(*args, conn=None):
    return Function(420, *args, conn=conn)

def MAKE_DEPENDENCY(*args, conn=None):
    return Function(421, *args, conn=conn)

def MAKE_DIM(*args, conn=None):
    return Function(422, *args, conn=conn)

def MAKE_DISPATCH(*args, conn=None):
    return Function(423, *args, conn=conn)

def MAKE_FUNCTION(*args, conn=None):
    return Function(424, *args, conn=conn)

def MAKE_METHOD(*args, conn=None):
    return Function(425, *args, conn=conn)

def MAKE_PARAM(*args, conn=None):
    return Function(426, *args, conn=conn)

def MAKE_PROCEDURE(*args, conn=None):
    return Function(427, *args, conn=conn)

def MAKE_PROGRAM(*args, conn=None):
    return Function(428, *args, conn=conn)

def MAKE_RANGE(*args, conn=None):
    return Function(429, *args, conn=conn)

def MAKE_ROUTINE(*args, conn=None):
    return Function(430, *args, conn=conn)

def MAKE_SIGNAL(*args, conn=None):
    return Function(431, *args, conn=conn)

def MAKE_WINDOW(*args, conn=None):
    return Function(432, *args, conn=conn)

def MAKE_WITH_UNITS(*args, conn=None):
    return Function(433, *args, conn=conn)

def MAKE_CALL(*args, conn=None):
    return Function(434, *args, conn=conn)

def CLASS_OF(*args, conn=None):
    return Function(435, *args, conn=conn)

def DSCPTR_OF(*args, conn=None):
    return Function(436, *args, conn=conn)

def KIND_OF(*args, conn=None):
    return Function(437, *args, conn=conn)

def NDESC_OF(*args, conn=None):
    return Function(438, *args, conn=conn)

def ACCUMULATE(*args, conn=None):
    return Function(439, *args, conn=conn)

def MAKE_SLOPE(*args, conn=None):
    return Function(440, *args, conn=conn)

def REM(*args, conn=None):
    return Function(441, *args, conn=conn)

def COMPLETION_MESSAGE_OF(*args, conn=None):
    return Function(442, *args, conn=conn)

def INTERRUPT_OF(*args, conn=None):
    return Function(443, *args, conn=conn)

def dSHOTNAME(conn=None):
    return Function(444, conn=conn)

def BUILD_WITH_ERROR(*args, conn=None):
    return Function(445, *args, conn=conn)

def ERROR_OF(*args, conn=None):
    return Function(446, *args, conn=conn)

def MAKE_WITH_ERROR(*args, conn=None):
    return Function(447, *args, conn=conn)

def DO_TASK(*args, conn=None):
    return Function(448, *args, conn=conn)

def ISQL_SET(*args, conn=None):
    return Function(449, *args, conn=conn)

def FS_FLOAT(*args, conn=None):
    return Function(450, *args, conn=conn)

def FS_COMPLEX(*args, conn=None):
    return Function(451, *args, conn=conn)

def FT_FLOAT(*args, conn=None):
    return Function(452, *args, conn=conn)

def FT_COMPLEX(*args, conn=None):
    return Function(453, *args, conn=conn)

def BUILD_OPAQUE(*args, conn=None):
    return Function(454, *args, conn=conn)

def MAKE_OPAQUE(*args, conn=None):
    return Function(455, *args, conn=conn)

def DICT(*args, conn=None):
    return Function(456, *args, conn=conn)

def TUPLE(*args, conn=None):
    return Function(457, *args, conn=conn)

def LIST(*args, conn=None):
    return Function(458, *args, conn=conn)

def SQUEEZE(*args, conn=None):
    return Function(459, *args, conn=conn)

def FLATTEN(*args, conn=None):
    return Function(460, *args, conn=conn)

