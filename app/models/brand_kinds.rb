class BrandKinds < ActiveHash::Base
  self.data = [
    { id: 0, name: '---' },
    { id: 5, name: 'シュライヒ' }, { id: 15, name: 'リーデル' }, { id: 25, name: 'ナハトマン' },
    { id: 35, name: 'カリマー' }, { id: 45, name: 'ペニー' }, { id: 55, name: 'sigg' },
    { id: 65, name: 'ペトロマックス' }
  ]
end
