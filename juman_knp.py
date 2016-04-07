# -*- coding: utf-8 -*-
import subprocess as sb

class JumanKnp:
  def __init__(self, text):
    self.text = text
    self.results = None
    self.pronunciation = ''

  def execute(self, juman_options=["-b"], knp_options=["-tab"]):
    cmd = 'echo %s | juman %s | knp %s' % (self.text, ' '.join(juman_options), ' '.join(knp_options))
    lines = sb.check_output(cmd, shell=True).split('\n')[:-2]
    self.results = Results(lines)

  def set_text(self, text):
    self.text = text

  def get_yomi(self):
    if len(self.results.bunsetsus) == 0:
      return None
    else:
      return self.results.yomi

  def get_words(self):
    words = []
    for b in self.results.bunsetsus:
      for w in b.words:
        words.append(w)
    return words


class Results:
  def __init__(self, lines):
    self.bunsetsus = []
    bunsetsu_idxes = [idx for idx, l in enumerate(lines) if l[0] == '*']
    copy_idxes = bunsetsu_idxes[1:] + [len(lines)]
    for idx, next_idx in zip(bunsetsu_idxes, copy_idxes):
      self.bunsetsus.append(Bunsetsu(lines[idx:next_idx]))
    self.yomi = ''.join([b.yomi for b in self.bunsetsus])

  def set_yomi(self, yomi):
    self.yomi = yomi

class Bunsetsu:
  def __init__(self, lines):
    self.text = ''.join([l.split(' ')[0] for l in lines if l[0] not in ['*', '+']])
    self.words = []
    for line in lines:
      outputs = line.split(' ')
      if outputs[0] in ['*', '+']:
        continue
      self.words.append(Word(line))
    self.yomi = ''.join([w.yomi for w in self.words])

class Word:
  def __init__(self, line):
    outputs = line.split(' ')
    self.text = outputs[0]
    self.yomi = outputs[1]
    self.original = outputs[2]
    self.pos = outputs[3]
    self.full_pos = outputs[5]
    self.pronunciation = ''
    # juman info
    if '"' in line:
      self.semantic_info = line[line.index('"')+1:line.rindex('"')]
    else:
      self.semantic_info = None
    # knp info
    if '<' in line and '>' in line:
      self.knp_info = line[line.index('<')+1:line.rindex('>')].split('><')
    else:
      self.knp_info = None
    self.is_symbol = True if self.pos == '特殊' else False
