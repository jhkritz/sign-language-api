import {
  mount,
  createLocalVue
} from '@vue/test-utils'
import Vue from 'vue'
import Vuetify from 'vuetify'
import libraryCard from '@/components/library-card.vue'

const localVue = createLocalVue()

describe('library-card.vue', () => {
  let vuetify

  beforeEach(() => {
    vuetify = new Vuetify()
  })
  it('renders card with library info', () => {
    const wrapper = mount(libraryCard, {
      propsData: { 
        libraryname: 'Test Library',
        librarydesc: 'Description',
       }
    })
    const title = wrapper.find('.v-card__title > span')
    expect(title.text()).toBe('Test Library')
  })
})
