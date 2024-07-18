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

def d():
    return Function(0)

def dA0():
    return Function(1)

def dALPHA():
    return Function(2)

def dAMU():
    return Function(3)

def dC():
    return Function(4)

def dCAL():
    return Function(5)

def dDEGREE():
    return Function(6)

def dEV():
    return Function(7)

def dFALSE():
    return Function(8)

def dFARADAY():
    return Function(9)

def dG():
    return Function(10)

def dGAS():
    return Function(11)

def dH():
    return Function(12)

def dHBAR():
    return Function(13)

def dI():
    return Function(14)

def dK():
    return Function(15)

def dME():
    return Function(16)

def dMISSING():
    return Function(17)

def dMP():
    return Function(18)

def dN0():
    return Function(19)

def dNA():
    return Function(20)

def dP0():
    return Function(21)

def dPI():
    return Function(22)

def dQE():
    return Function(23)

def dRE():
    return Function(24)

def dROPRAND():
    return Function(25)

def dRYDBERG():
    return Function(26)

def dT0():
    return Function(27)

def dTORR():
    return Function(28)

def dTRUE():
    return Function(29)

def dVALUE():
    return Function(30)

def ABORT(*args):
    return Function(31, *args)

def ABS(*args):
    return Function(32, *args)

def ABS1(*args):
    return Function(33, *args)

def ABSSQ(*args):
    return Function(34, *args)

def ACHAR(*args):
    return Function(35, *args)

def ACOS(*args):
    return Function(36, *args)

def ACOSD(*args):
    return Function(37, *args)

def ADD(*args):
    return Function(38, *args)

def ADJUSTL(*args):
    return Function(39, *args)

def ADJUSTR(*args):
    return Function(40, *args)

def AIMAG(*args):
    return Function(41, *args)

def AINT(*args):
    return Function(42, *args)

def ALL(*args):
    return Function(43, *args)

def ALLOCATED(*args):
    return Function(44, *args)

def AND(*args):
    return Function(45, *args)

def AND_NOT(*args):
    return Function(46, *args)

def ANINT(*args):
    return Function(47, *args)

def ANY(*args):
    return Function(48, *args)

def ARG(*args):
    return Function(49, *args)

def ARGD(*args):
    return Function(50, *args)

def ARG_OF(*args):
    return Function(51, *args)

def ARRAY(*args):
    return Function(52, *args)

def ASIN(*args):
    return Function(53, *args)

def ASIND(*args):
    return Function(54, *args)

def AS_IS(*args):
    return Function(55, *args)

def ATAN(*args):
    return Function(56, *args)

def ATAN2(*args):
    return Function(57, *args)

def ATAN2D(*args):
    return Function(58, *args)

def ATAND(*args):
    return Function(59, *args)

def ATANH(*args):
    return Function(60, *args)

def AXIS_OF(*args):
    return Function(61, *args)

def BACKSPACE(*args):
    return Function(62, *args)

def IBCLR(*args):
    return Function(63, *args)

def BEGIN_OF(*args):
    return Function(64, *args)

def IBITS(*args):
    return Function(65, *args)

def BREAK():
    return Function(66)

def BSEARCH(*args):
    return Function(67, *args)

def IBSET(*args):
    return Function(68, *args)

def BTEST(*args):
    return Function(69, *args)

def BUILD_ACTION(*args):
    return Function(70, *args)

def BUILD_CONDITION(*args):
    return Function(71, *args)

def BUILD_CONGLOM(*args):
    return Function(72, *args)

def BUILD_DEPENDENCY(*args):
    return Function(73, *args)

def BUILD_DIM(*args):
    return Function(74, *args)

def BUILD_DISPATCH(*args):
    return Function(75, *args)

def BUILD_EVENT(*args):
    return Function(76, *args)

def BUILD_FUNCTION(*args):
    return Function(77, *args)

def BUILD_METHOD(*args):
    return Function(78, *args)

def BUILD_PARAM(*args):
    return Function(79, *args)

def BUILD_PATH(*args):
    return Function(80, *args)

def BUILD_PROCEDURE(*args):
    return Function(81, *args)

def BUILD_PROGRAM(*args):
    return Function(82, *args)

def BUILD_RANGE(*args):
    return Function(83, *args)

def BUILD_ROUTINE(*args):
    return Function(84, *args)

def BUILD_SIGNAL(*args):
    return Function(85, *args)

def BUILD_SLOPE(*args):
    return Function(86, *args)

def BUILD_WINDOW(*args):
    return Function(87, *args)

def BUILD_WITH_UNITS(*args):
    return Function(88, *args)

def BUILTIN_OPCODE(*args):
    return Function(89, *args)

def BYTE(*args):
    return Function(90, *args)

def BYTE_UNSIGNED(*args):
    return Function(91, *args)

def CASE(*args):
    return Function(92, *args)

def CEILING(*args):
    return Function(93, *args)

def CHAR(*args):
    return Function(94, *args)

def CLASS(*args):
    return Function(95, *args)

def FCLOSE(*args):
    return Function(96, *args)

def CMPLX(*args):
    return Function(97, *args)

def COMMA(*args):
    return Function(98, *args)

def COMPILE(*args):
    return Function(99, *args)

def COMPLETION_OF(*args):
    return Function(100, *args)

def CONCAT(*args):
    return Function(101, *args)

def CONDITIONAL(*args):
    return Function(102, *args)

def CONJG(*args):
    return Function(103, *args)

def CONTINUE():
    return Function(104)

def CONVOLVE(*args):
    return Function(105, *args)

def COS(*args):
    return Function(106, *args)

def COSD(*args):
    return Function(107, *args)

def COSH(*args):
    return Function(108, *args)

def COUNT(*args):
    return Function(109, *args)

def CSHIFT(*args):
    return Function(110, *args)

def CVT(*args):
    return Function(111, *args)

def DATA(*args):
    return Function(112, *args)

def DATE_AND_TIME(*args):
    return Function(113, *args)

def DATE_TIME(*args):
    return Function(114, *args)

def DBLE(*args):
    return Function(115, *args)

def DEALLOCATE(*args):
    return Function(116, *args)

def DEBUG(*args):
    return Function(117, *args)

def DECODE(*args):
    return Function(118, *args)

def DECOMPILE(*args):
    return Function(119, *args)

def DECOMPRESS(*args):
    return Function(120, *args)

def DEFAULT(*args):
    return Function(121, *args)

def DERIVATIVE(*args):
    return Function(122, *args)

def DESCR(*args):
    return Function(123, *args)

def DIAGONAL(*args):
    return Function(124, *args)

def DIGITS(*args):
    return Function(125, *args)

def DIM(*args):
    return Function(126, *args)

def DIM_OF(*args):
    return Function(127, *args)

def DISPATCH_OF(*args):
    return Function(128, *args)

def DIVIDE(*args):
    return Function(129, *args)

def LBOUND(*args):
    return Function(130, *args)

def DO(*args):
    return Function(131, *args)

def DOT_PRODUCT(*args):
    return Function(132, *args)

def DPROD(*args):
    return Function(133, *args)

def DSCPTR(*args):
    return Function(134, *args)

def SHAPE(*args):
    return Function(135, *args)

def SIZE(*args):
    return Function(136, *args)

def KIND(*args):
    return Function(137, *args)

def UBOUND(*args):
    return Function(138, *args)

def D_COMPLEX(*args):
    return Function(139, *args)

def D_FLOAT(*args):
    return Function(140, *args)

def RANGE(*args):
    return Function(141, *args)

def PRECISION(*args):
    return Function(142, *args)

def ELBOUND(*args):
    return Function(143, *args)

def ELSE():
    return Function(144)

def ELSEWHERE():
    return Function(145)

def ENCODE(*args):
    return Function(146, *args)

def ENDFILE(*args):
    return Function(147, *args)

def END_OF(*args):
    return Function(148, *args)

def EOSHIFT(*args):
    return Function(149, *args)

def EPSILON(*args):
    return Function(150, *args)

def EQ(*args):
    return Function(151, *args)

def EQUALS(*args):
    return Function(152, *args)

def EQUALS_FIRST(*args):
    return Function(153, *args)

def EQV(*args):
    return Function(154, *args)

def ESHAPE(*args):
    return Function(155, *args)

def ESIZE(*args):
    return Function(156, *args)

def EUBOUND(*args):
    return Function(157, *args)

def EVALUATE(*args):
    return Function(158, *args)

def EXECUTE(*args):
    return Function(159, *args)

def EXP(*args):
    return Function(160, *args)

def EXPONENT(*args):
    return Function(161, *args)

def EXT_FUNCTION(*args):
    return Function(162, *args)

def FFT(*args):
    return Function(163, *args)

def FIRSTLOC(*args):
    return Function(164, *args)

def FIT(*args):
    return Function(165, *args)

def FIX_ROPRAND(*args):
    return Function(166, *args)

def FLOAT(*args):
    return Function(167, *args)

def FLOOR(*args):
    return Function(168, *args)

def FOR(*args):
    return Function(169, *args)

def FRACTION(*args):
    return Function(170, *args)

def FUN(*args):
    return Function(171, *args)

def F_COMPLEX(*args):
    return Function(172, *args)

def F_FLOAT(*args):
    return Function(173, *args)

def GE(*args):
    return Function(174, *args)

def GETNCI(*args):
    return Function(175, *args)

def GOTO(*args):
    return Function(176, *args)

def GT(*args):
    return Function(177, *args)

def G_COMPLEX(*args):
    return Function(178, *args)

def G_FLOAT(*args):
    return Function(179, *args)

def HELP_OF(*args):
    return Function(180, *args)

def HUGE(*args):
    return Function(181, *args)

def H_COMPLEX(*args):
    return Function(182, *args)

def H_FLOAT(*args):
    return Function(183, *args)

def IACHAR(*args):
    return Function(184, *args)

def IAND(*args):
    return Function(185, *args)

def IAND_NOT(*args):
    return Function(186, *args)

def ICHAR(*args):
    return Function(187, *args)

def IDENT_OF(*args):
    return Function(188, *args)

def IF(*args):
    return Function(189, *args)

def IF_ERROR(*args):
    return Function(190, *args)

def IMAGE_OF(*args):
    return Function(191, *args)

def IN(*args):
    return Function(192, *args)

def INAND(*args):
    return Function(193, *args)

def INAND_NOT(*args):
    return Function(194, *args)

def INDEX(*args):
    return Function(195, *args)

def INOR(*args):
    return Function(196, *args)

def INOR_NOT(*args):
    return Function(197, *args)

def INOT(*args):
    return Function(198, *args)

def INOUT(*args):
    return Function(199, *args)

def INQUIRE(*args):
    return Function(200, *args)

def INT(*args):
    return Function(201, *args)

def INTEGRAL(*args):
    return Function(202, *args)

def INTERPOL(*args):
    return Function(203, *args)

def INTERSECT(*args):
    return Function(204, *args)

def INT_UNSIGNED(*args):
    return Function(205, *args)

def INVERSE(*args):
    return Function(206, *args)

def IOR(*args):
    return Function(207, *args)

def IOR_NOT(*args):
    return Function(208, *args)

def IS_IN(*args):
    return Function(209, *args)

def IEOR(*args):
    return Function(210, *args)

def IEOR_NOT(*args):
    return Function(211, *args)

def LABEL(*args):
    return Function(212, *args)

def LAMINATE(*args):
    return Function(213, *args)

def LANGUAGE_OF(*args):
    return Function(214, *args)

def LASTLOC(*args):
    return Function(215, *args)

def LE(*args):
    return Function(216, *args)

def LEN(*args):
    return Function(217, *args)

def LEN_TRIM(*args):
    return Function(218, *args)

def LGE(*args):
    return Function(219, *args)

def LGT(*args):
    return Function(220, *args)

def LLE(*args):
    return Function(221, *args)

def LLT(*args):
    return Function(222, *args)

def LOG(*args):
    return Function(223, *args)

def LOG10(*args):
    return Function(224, *args)

def LOG2(*args):
    return Function(225, *args)

def LOGICAL(*args):
    return Function(226, *args)

def LONG(*args):
    return Function(227, *args)

def LONG_UNSIGNED(*args):
    return Function(228, *args)

def LT(*args):
    return Function(229, *args)

def MATMUL(*args):
    return Function(230, *args)

def MAT_ROT(*args):
    return Function(231, *args)

def MAT_ROT_INT(*args):
    return Function(232, *args)

def MAX(*args):
    return Function(233, *args)

def MAXEXPONENT(*args):
    return Function(234, *args)

def MAXLOC(*args):
    return Function(235, *args)

def MAXVAL(*args):
    return Function(236, *args)

def MEAN(*args):
    return Function(237, *args)

def MEDIAN(*args):
    return Function(238, *args)

def MERGE(*args):
    return Function(239, *args)

def METHOD_OF(*args):
    return Function(240, *args)

def MIN(*args):
    return Function(241, *args)

def MINEXPONENT(*args):
    return Function(242, *args)

def MINLOC(*args):
    return Function(243, *args)

def MINVAL(*args):
    return Function(244, *args)

def MOD(*args):
    return Function(245, *args)

def MODEL_OF(*args):
    return Function(246, *args)

def MULTIPLY(*args):
    return Function(247, *args)

def NAME_OF(*args):
    return Function(248, *args)

def NAND(*args):
    return Function(249, *args)

def NAND_NOT(*args):
    return Function(250, *args)

def NDESC(*args):
    return Function(251, *args)

def NE(*args):
    return Function(252, *args)

def NEAREST(*args):
    return Function(253, *args)

def NEQV(*args):
    return Function(254, *args)

def NINT(*args):
    return Function(255, *args)

def NOR(*args):
    return Function(256, *args)

def NOR_NOT(*args):
    return Function(257, *args)

def NOT(*args):
    return Function(258, *args)

def OBJECT_OF(*args):
    return Function(259, *args)

def OCTAWORD(*args):
    return Function(260, *args)

def OCTAWORD_UNSIGNED(*args):
    return Function(261, *args)

def ON_ERROR(*args):
    return Function(262, *args)

def OPCODE_BUILTIN(*args):
    return Function(263, *args)

def OPCODE_STRING(*args):
    return Function(264, *args)

def FOPEN(*args):
    return Function(265, *args)

def OPTIONAL(*args):
    return Function(266, *args)

def OR(*args):
    return Function(267, *args)

def OR_NOT(*args):
    return Function(268, *args)

def OUT(*args):
    return Function(269, *args)

def PACK(*args):
    return Function(270, *args)

def PHASE_OF(*args):
    return Function(271, *args)

def POST_DEC(*args):
    return Function(272, *args)

def POST_INC(*args):
    return Function(273, *args)

def POWER(*args):
    return Function(274, *args)

def PRESENT(*args):
    return Function(275, *args)

def PRE_DEC(*args):
    return Function(276, *args)

def PRE_INC(*args):
    return Function(277, *args)

def PRIVATE(*args):
    return Function(278, *args)

def PROCEDURE_OF(*args):
    return Function(279, *args)

def PRODUCT(*args):
    return Function(280, *args)

def PROGRAM_OF(*args):
    return Function(281, *args)

def PROJECT(*args):
    return Function(282, *args)

def PROMOTE(*args):
    return Function(283, *args)

def PUBLIC(*args):
    return Function(284, *args)

def QUADWORD(*args):
    return Function(285, *args)

def QUADWORD_UNSIGNED(*args):
    return Function(286, *args)

def QUALIFIERS_OF(*args):
    return Function(287, *args)

def RADIX(*args):
    return Function(288, *args)

def RAMP(*args):
    return Function(289, *args)

def RANDOM(*args):
    return Function(290, *args)

def RANDOM_SEED(*args):
    return Function(291, *args)

def DTYPE_RANGE(*args):
    return Function(292, *args)

def RANK(*args):
    return Function(293, *args)

def RAW_OF(*args):
    return Function(294, *args)

def READ(*args):
    return Function(295, *args)

def REAL(*args):
    return Function(296, *args)

def REBIN(*args):
    return Function(297, *args)

def REF(*args):
    return Function(298, *args)

def REPEAT(*args):
    return Function(299, *args)

def REPLICATE(*args):
    return Function(300, *args)

def RESHAPE(*args):
    return Function(301, *args)

def RETURN(*args):
    return Function(302, *args)

def REWIND(*args):
    return Function(303, *args)

def RMS(*args):
    return Function(304, *args)

def ROUTINE_OF(*args):
    return Function(305, *args)

def RRSPACING(*args):
    return Function(306, *args)

def SCALE(*args):
    return Function(307, *args)

def SCAN(*args):
    return Function(308, *args)

def FSEEK(*args):
    return Function(309, *args)

def SET_EXPONENT(*args):
    return Function(310, *args)

def SET_RANGE(*args):
    return Function(311, *args)

def ISHFT(*args):
    return Function(312, *args)

def ISHFTC(*args):
    return Function(313, *args)

def SHIFT_LEFT(*args):
    return Function(314, *args)

def SHIFT_RIGHT(*args):
    return Function(315, *args)

def SIGN(*args):
    return Function(316, *args)

def SIGNED(*args):
    return Function(317, *args)

def SIN(*args):
    return Function(318, *args)

def SIND(*args):
    return Function(319, *args)

def SINH(*args):
    return Function(320, *args)

def SIZEOF(*args):
    return Function(321, *args)

def SLOPE_OF(*args):
    return Function(322, *args)

def SMOOTH(*args):
    return Function(323, *args)

def SOLVE(*args):
    return Function(324, *args)

def SORTVAL(*args):
    return Function(325, *args)

def SPACING(*args):
    return Function(326, *args)

def SPAWN(*args):
    return Function(327, *args)

def SPREAD(*args):
    return Function(328, *args)

def SQRT(*args):
    return Function(329, *args)

def SQUARE(*args):
    return Function(330, *args)

def STATEMENT(*args):
    return Function(331, *args)

def STD_DEV(*args):
    return Function(332, *args)

def STRING(*args):
    return Function(333, *args)

def STRING_OPCODE(*args):
    return Function(334, *args)

def SUBSCRIPT(*args):
    return Function(335, *args)

def SUBTRACT(*args):
    return Function(336, *args)

def SUM(*args):
    return Function(337, *args)

def SWITCH(*args):
    return Function(338, *args)

def SYSTEM_CLOCK(*args):
    return Function(339, *args)

def TAN(*args):
    return Function(340, *args)

def TAND(*args):
    return Function(341, *args)

def TANH(*args):
    return Function(342, *args)

def TASK_OF(*args):
    return Function(343, *args)

def TEXT(*args):
    return Function(344, *args)

def TIME_OUT_OF(*args):
    return Function(345, *args)

def TINY(*args):
    return Function(346, *args)

def TRANSFER(*args):
    return Function(347, *args)

def TRANSPOSE_(*args):
    return Function(348, *args)

def TRIM(*args):
    return Function(349, *args)

def UNARY_MINUS(*args):
    return Function(350, *args)

def UNARY_PLUS(*args):
    return Function(351, *args)

def UNION(*args):
    return Function(352, *args)

def UNITS(*args):
    return Function(353, *args)

def UNITS_OF(*args):
    return Function(354, *args)

def UNPACK(*args):
    return Function(355, *args)

def UNSIGNED(*args):
    return Function(356, *args)

def VAL(*args):
    return Function(357, *args)

def VALIDATION_OF(*args):
    return Function(358, *args)

def VALUE_OF(*args):
    return Function(359, *args)

def VAR(*args):
    return Function(360, *args)

def VECTOR(*args):
    return Function(361, *args)

def VERIFY(*args):
    return Function(362, *args)

def WAIT(*args):
    return Function(363, *args)

def WHEN_OF(*args):
    return Function(364, *args)

def WHERE(*args):
    return Function(365, *args)

def WHILE(*args):
    return Function(366, *args)

def WINDOW_OF(*args):
    return Function(367, *args)

def WORD(*args):
    return Function(368, *args)

def WORD_UNSIGNED(*args):
    return Function(369, *args)

def WRITE(*args):
    return Function(370, *args)

def ZERO(*args):
    return Function(371, *args)

def d2PI():
    return Function(372)

def dNARG():
    return Function(373)

def ELEMENT(*args):
    return Function(374, *args)

def RC_DROOP(*args):
    return Function(375, *args)

def RESET_PRIVATE():
    return Function(376)

def RESET_PUBLIC():
    return Function(377)

def SHOW_PRIVATE(*args):
    return Function(378, *args)

def SHOW_PUBLIC(*args):
    return Function(379, *args)

def SHOW_VM(*args):
    return Function(380, *args)

def TRANSLATE(*args):
    return Function(381, *args)

def TRANSPOSE_MUL(*args):
    return Function(382, *args)

def UPCASE(*args):
    return Function(383, *args)

def USING(*args):
    return Function(384, *args)

def VALIDATION(*args):
    return Function(385, *args)

def dDEFAULT():
    return Function(386)

def dEXPT():
    return Function(387)

def dSHOT():
    return Function(388)

def GETDBI(*args):
    return Function(389, *args)

def CULL(*args):
    return Function(390, *args)

def EXTEND(*args):
    return Function(391, *args)

def I_TO_X(*args):
    return Function(392, *args)

def X_TO_I(*args):
    return Function(393, *args)

def MAP(*args):
    return Function(394, *args)

def COMPILE_DEPENDENCY(*args):
    return Function(395, *args)

def DECOMPILE_DEPENDENCY(*args):
    return Function(396, *args)

def BUILD_CALL(*args):
    return Function(397, *args)

def ERRORLOGS_OF(*args):
    return Function(398, *args)

def PERFORMANCE_OF(*args):
    return Function(399, *args)

def XD(*args):
    return Function(400, *args)

def CONDITION_OF(*args):
    return Function(401, *args)

def SORT(*args):
    return Function(402, *args)

def dTHIS():
    return Function(403)

def DATA_WITH_UNITS(*args):
    return Function(404, *args)

def dATM():
    return Function(405)

def dEPSILON0():
    return Function(406)

def dGN():
    return Function(407)

def dMU0():
    return Function(408)

def EXTRACT(*args):
    return Function(409, *args)

def FINITE(*args):
    return Function(410, *args)

def BIT_SIZE(*args):
    return Function(411, *args)

def MODULO(*args):
    return Function(412, *args)

def SELECTED_INT_KIND(*args):
    return Function(413, *args)

def SELECTED_REAL_KIND(*args):
    return Function(414, *args)

def DSQL(*args):
    return Function(415, *args)

def ISQL(*args):
    return Function(416, *args)

def FTELL(*args):
    return Function(417, *args)

def MAKE_ACTION(*args):
    return Function(418, *args)

def MAKE_CONDITION(*args):
    return Function(419, *args)

def MAKE_CONGLOM(*args):
    return Function(420, *args)

def MAKE_DEPENDENCY(*args):
    return Function(421, *args)

def MAKE_DIM(*args):
    return Function(422, *args)

def MAKE_DISPATCH(*args):
    return Function(423, *args)

def MAKE_FUNCTION(*args):
    return Function(424, *args)

def MAKE_METHOD(*args):
    return Function(425, *args)

def MAKE_PARAM(*args):
    return Function(426, *args)

def MAKE_PROCEDURE(*args):
    return Function(427, *args)

def MAKE_PROGRAM(*args):
    return Function(428, *args)

def MAKE_RANGE(*args):
    return Function(429, *args)

def MAKE_ROUTINE(*args):
    return Function(430, *args)

def MAKE_SIGNAL(*args):
    return Function(431, *args)

def MAKE_WINDOW(*args):
    return Function(432, *args)

def MAKE_WITH_UNITS(*args):
    return Function(433, *args)

def MAKE_CALL(*args):
    return Function(434, *args)

def CLASS_OF(*args):
    return Function(435, *args)

def DSCPTR_OF(*args):
    return Function(436, *args)

def KIND_OF(*args):
    return Function(437, *args)

def NDESC_OF(*args):
    return Function(438, *args)

def ACCUMULATE(*args):
    return Function(439, *args)

def MAKE_SLOPE(*args):
    return Function(440, *args)

def REM(*args):
    return Function(441, *args)

def COMPLETION_MESSAGE_OF(*args):
    return Function(442, *args)

def INTERRUPT_OF(*args):
    return Function(443, *args)

def dSHOTNAME():
    return Function(444)

def BUILD_WITH_ERROR(*args):
    return Function(445, *args)

def ERROR_OF(*args):
    return Function(446, *args)

def MAKE_WITH_ERROR(*args):
    return Function(447, *args)

def DO_TASK(*args):
    return Function(448, *args)

def ISQL_SET(*args):
    return Function(449, *args)

def FS_FLOAT(*args):
    return Function(450, *args)

def FS_COMPLEX(*args):
    return Function(451, *args)

def FT_FLOAT(*args):
    return Function(452, *args)

def FT_COMPLEX(*args):
    return Function(453, *args)

def BUILD_OPAQUE(*args):
    return Function(454, *args)

def MAKE_OPAQUE(*args):
    return Function(455, *args)

def DICT(*args):
    return Function(456, *args)

def TUPLE(*args):
    return Function(457, *args)

def LIST(*args):
    return Function(458, *args)

def SQUEEZE(*args):
    return Function(459, *args)

def FLATTEN(*args):
    return Function(460, *args)

